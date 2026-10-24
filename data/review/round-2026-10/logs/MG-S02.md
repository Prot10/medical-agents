# MG-S02
Reviewer status: none (MG not reviewed in this round; July 2026 tool review only) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| none: no reviewer notes for this case | - | - |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness` | Timeline leak: "thyroid function tests performed 2 weeks ago were normal (TSH 2.2)" while TSH is part of the scored labs criterion. | FIXED: sentence removed; the ophthalmologist's referral kept. |
| D | major | `patient.neurological_exam.additional` | "NIF -61 cmH2O (normal)" in the patient block while respiratory function is scored (plan K). | FIXED: deleted. |
| B | major | `patient.neurological_exam.cranial_nerves` | Garbled ocular motor statement ("left medial rectus/adductor weakness causing false impression of esotropia, actually left lateral rectus weakness"): left lateral rectus weakness gives diplopia on leftward gaze, but the HPI reports diplopia looking right. | FIXED: limited adduction of the left eye with horizontal diplopia on rightward gaze; vertical diplopia on upgaze kept. |
| C | minor | `patient.neurological_exam.cranial_nerves` | Ptosis given as levator excursion; clinical activity score sat in a lab panel (plan H8). | FIXED: MRD1 left 1.5 mm, right 3.5 mm; "no proptosis, lid retraction, chemosis or eyelid oedema (clinical activity score 0/7)" in the exam. |
| B | minor | `patient.physical_exam` (absent) | No weight for the respiratory mL/kg value (plan fact 14). | FIXED: physical exam added (weight 65.4 kg, height 163 cm matching BMI 24.6; neck, cardiovascular, respiratory, abdomen). |
| A | major | `initial_tool_outputs.ct`, `followup_outputs[request_thymectomy_evaluation]` | Chest CT stored in the head-CT slot; a second "repeat" chest CT in a body-imaging follow-up (plan H3). | FIXED: one `initial_tool_outputs.body_imaging` report (contrast CT, region "chest, anterior mediastinum": residual thymic tissue for age, no thymoma, no nodes, lungs clear); `initial_tool_outputs.ct` null (library answers a head CT); follow-up deleted. |
| A | major | `followup_outputs[request_graves_thyroid_eye_disease_exclusion]` | Labs follow-up duplicating TRAb, holding anti-TPO and an exam score (CAS) (plan H8). | FIXED: deleted; anti-TPO 62 IU/mL (H) moved into the initial thyroid panel; TRAb kept there once; CAS moved to the exam. |
| B | major | `initial_tool_outputs.labs` | CBC and BMP "All normal"; two laboratories (AChR < 0.5, MuSK < 0.02); MuSK in an AChR-positive patient; anti-titin (not orderable) (plan G, fact 2, H9, CENTRAL 7). | FIXED: analytes with values; one laboratory (AChR binding <= 0.02 nmol/L); MuSK and titin removed; values kept (8.7 nmol/L, 62%, 78%, TSH 2.2, free T4 1.2, TRAb 0.4). |
| C | major | `initial_tool_outputs.specialized_test` | Edrophonium test reported (plan fact 9); no technique or exercise testing. | FIXED: Tensilon removed; structured RNS with technique, baseline CMAPs, 3 Hz decrements unchanged (orbicularis oculi 20%, deltoid 15%, masseter 24%), post-exercise deltoid 4% (no facilitation), normal NCS. |
| C | major | ice pack (no criterion, no report; `metadata.actions_withdrawn`) | Fatigable ptosis without the recommended ice pack test (plan 3.5). | FIXED: recommended criterion `action-ice-pack-test`, follow-up report (left MRD1 1.5 to 4.0 mm); `actions_withdrawn` removed. |
| C | major | `followup_outputs[request_mgtx_trial_evidence]` | Literature output with wrong facts ("MGTX 5-year, Lancet Neurology 2022", "regardless of CT findings"), plan B and fact 23. | FIXED: deleted with the literature criterion. |
| C | minor | `followup_outputs[request_pyridostigmine_levothyroxine]` | Treatment plan in `proposed`; corticosteroid-levothyroxine absorption claim unsupported; no MG-relevant interaction with levothyroxine (plan 3.2). | FIXED: deleted with the drug criterion (library answers any check). |
| C | minor | `followup_outputs[request_respiratory_function]`, `[request_emg_single_fiber]` | Respiratory report without units, % predicted or mL/kg; SFEMG without muscle, blocking 17/20 equal to the jitter count. | FIXED: FVC 3.62 L (102%, 55 mL/kg), MIP -72, MEP 88 cmH2O, SBC 38; SFEMG frontalis 20 pairs, MCD 82 microseconds, jitter 17/20, blocking 8/20. |
| A | major | `ground_truth.action_criteria` | Template criteria (labs with MuSK/LRP4, literature and drug check required, labels equal to rationales, `[Wolfe_2016]` everywhere) (plan A, N). | FIXED: labs `[anti_AChR, TSH]` required; RNS required; SFEMG optional; ice pack recommended; mediastinal imaging required (alternatives mediastinum_MRI, chest_CT); respiratory recommended; literature and drug checks removed; case-specific text. |
| B | minor | `ground_truth.sequence_constraints`, `stop_rule` | `labs -> RNS` with an SFEMG reason; literature and drug check required before assessment; `max_additional_actions: 0`. | FIXED: `RNS -> SFEMG` and `labs -> SFEMG` soft; stop rule labs, RNS, imaging; `max_additional_actions: 1`. |
| C | major | `ground_truth.assessment.required_recommendations` | Diagnostic musts (confirm AChR, CT, "Single-fiber EMG given diagnostic clarity"); vague endocrinology steroid coordination; no thymectomy or steroid plan (plan D). | FIXED: pyridostigmine titration; low-dose prednisone escalation, azathioprine after TPMT; elective thymectomy per MGTX with pre-operative IVIG/PLEX if bulbar weakness persists; pregnancy counselling (fact 19); euthyroid maintenance; drug list. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Seven template prohibitions incl. telithromycin. | FIXED: canonical three (functional/thyroid eye disease/allergy attribution) plus mycophenolate/methotrexate without contraception. |
| C | major | `ground_truth.differential` | Graves orbitopathy left moderate though TRAb is negative and the orbits are quiet; "Pregnancy-related fatigue" not raised by anything in the case; thyroid myopathy coded E07.1 (dyshormogenetic goitre) (ruling 7). | FIXED: Graves orbitopathy low with excluding features; pregnancy entry removed; thyroid myopathy E05.4 with normal TSH/free T4; LEMS features updated. |
| C | minor | `ground_truth.key_clinical_evidence[2..4]` | SFEMG ">95%", "All confirmed MG require CT chest", telithromycin (plan E). | FIXED: case-specific bullets. |
| E | minor | `ground_truth.avoided_actions[*]` | `[Wolfe_2016]` citations. | FIXED: emptied, case rationales with Jacob 2025 in text. |
| E | minor | `metadata` | Difficulty rationale, revision fields. | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

A 29-year-old woman with treated Graves disease (hypothyroid on levothyroxine) and generalized AChR-positive MG (IIb) without thymoma. The work-up is AChR antibody with thyroid function and antibodies (one report: AChR binding 8.7 nmol/L, blocking 62%, modulating 78%; TSH 2.2, free T4 1.2, TRAb negative, anti-TPO 62), RNS (decrement in orbicularis oculi, deltoid and masseter, no post-exercise facilitation; the Tensilon test removed), an ice pack test (left MRD1 1.5 to 4.0 mm), contrast CT of the chest and mediastinum moved out of the head-CT slot (no thymoma), and respiratory staging with weight-based values (normal). SFEMG is optional; literature and drug checks are no longer criteria (the literature output misdated the MGTX extension). The HPI no longer quotes her TSH, the exam no longer quotes the NIF, and the ocular motor findings now agree with diplopia on right gaze. Musts: pyridostigmine, low-dose prednisone escalation with azathioprine after TPMT if needed, elective thymectomy per MGTX, pregnancy counselling, euthyroid maintenance, drug counselling. Graves orbitopathy is now low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan CENTRAL 1: `[Jacob_2025]`, `[Evoli_2019]`, `[Lawn_2001]` in text only.
- Plan CENTRAL 2: `icd_codes[0]` G70.01 for a stable new diagnosis (G70.00 fits). Not changed.
- Plan CENTRAL 3: synonyms accept "ocular myasthenia gravis" for this generalized case.

## Open questions for Andrea (judgment calls you could not settle)

- None.

## Verification

Adversarial check, 24 Oct 2026. Read the log, the full diff and the final case. Confirmed: HPI no longer quotes the TSH; NIF gone; left adduction deficit with right-gaze diplopia matches the HPI; CAS moved to the exam; TRAb negative and anti-TPO 62 (H) in one thyroid panel; one laboratory for AChR; chest CT moved to body imaging with region answering mediastinum_CT and chest_CT; BMI 24.6 and FVC 55 mL/kg recomputed; Graves orbitopathy lowered with excluding features; thyroid myopathy E05.4 fits over-replacement; MGTX thymectomy must valid (29); pregnancy counselling per plan fact 19; leak guard passes.

Found and fixed:
- D minor: `fallback_tool_outputs.advanced_imaging.modality` was the prose "FDG-PET scan" (PATTERNS 5). Set to `FDG_PET` with a whole-body protocol; the normal result is consistent with no thymoma.

perfect_agent passes; case_io check clean for this case.

## Condition audit (MG auditor, 24 Oct 2026)

- fallback_tool_outputs.echo.echo_type set to TTE. FIXED.
  Why: the discriminator guard (PATTERNS.md section 5) requires an exact vocabulary value on every case fallback; an empty echo_type answered every echo variant. The RS11-RS16 verifiers fixed this only in their own cases.
- `perfect_agent.py` and `case_io.py check` re-run on all 30 MG cases after the changes; the hand-run discriminator guard reports 0 defects in the 30 MG cases.
