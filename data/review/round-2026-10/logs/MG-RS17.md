# MG-RS17
Reviewer status: none (MG not reviewed in this round; July 2026 tool review only) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| none: no reviewer notes for this case | - | - |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | major | `followup_outputs[request_achR_antibodies]`, `initial_tool_outputs.labs` | First-line serology sat in a follow-up behind a TSH stub; the initial labs held a duplicate stub TSH row ("Mimic exclusion", no value or unit) (plan H6, G). | FIXED: AChR binding/blocking/modulating panel moved into `initial_tool_outputs.labs`; stub panel deleted; follow-up deleted; anti-TPO (12 IU/mL, normal) added per the July 2026 guidance (thyroid antibodies in all patients). |
| C | minor | `initial_tool_outputs.labs` (formerly the follow-up) | Two laboratories in one report (AChR binding reference < 0.4 nmol/L, MuSK <= 0.02); MuSK and LRP4 reported in an AChR-positive patient, where they are not indicated (plan fact 1, 2, H9). | FIXED: one Mayo-style laboratory (binding <= 0.02 nmol/L, blocking <= 15%, modulating 0-20%); MuSK and LRP4 rows removed. |
| D | major | `patient.neurological_exam.additional` | "NIF -62 cmH2O" in the patient block while respiratory function is a scored criterion (plan K). | FIXED: deleted. |
| B | minor | `patient.neurological_exam.cranial_nerves` | "limitation of left eye adduction" with diplopia on leftward gaze, while the physical exam says left abduction limitation (diplopia on leftward gaze fits abduction). | FIXED: "abduction". |
| C | minor | `patient.neurological_exam.cranial_nerves`, `physical_exam.neurological`, ice pack follow-up | Ptosis and the ice pack response measured as levator excursion (a measure of levator function, not of ptosis); the ice pack test is read on MRD1 or palpebral fissure (plan fact 9, I). | FIXED: exam MRD1 1 mm left, 4 mm right; ice pack MRD1 1.0 to 3.5 mm (2.5 mm improvement), quantitative fields renamed, impression without interpretive sentence. |
| C | major | `followup_outputs[request_respiratory_function]` | NIF "threshold for concern < -60 cmH2O - adequate", no mL/kg, no weight in the case (plan fact 14). | FIXED: weight 72 kg and height 165 cm added to `physical_exam.general` (BMI 26.4 unchanged); report FVC 2.85 L, 95% predicted, 40 mL/kg; MIP -66 cmH2O; MEP 84 cmH2O; single-breath count 32; strong cough; no supine fall. |
| C | minor | `initial_tool_outputs.specialized_test` | 50 Hz high-rate RNS (painful, not needed) with the ">100%" cut-off (plan fact 8). | FIXED: replaced by brief-exercise testing (trapezius CMAP 6.8 to 7.3 mV, 7%, reference < 60%); "patient not taking pyridostigmine" added to technique; impression and quantitative data updated; LEMS differential and key evidence updated to match. |
| A | major | `ground_truth.action_criteria` | Template criteria: labs required `[anti_AChR, anti_MuSK, anti_LRP4, TSH]`, literature and generic pyridostigmine drug check (with telithromycin) required, labels equal to rationales, `[Wolfe_2016]` cited for serology, RNS, ice pack (plan A, N). | FIXED: labs `[anti_AChR, TSH]`; literature criterion and its follow-up deleted (plan default for a straightforward case; library answers any search); drug check deleted with its follow-up (losartan has no MG-relevant interaction, plan 3.2); order labs, RNS, ice pack, mediastinal CT, respiratory; labels imperative, rationales case-specific with sources in text; `[Wolfe_2016]` kept only on the mediastinal CT criterion (thymectomy decision); mediastinum_MRI and chest_CT with contrast added as alternatives (served by library normal reports, consistent with this normal CT). |
| B | minor | `ground_truth.sequence_constraints` | `labs -> RNS` constraint whose reason talks about SFEMG; no SFEMG criterion exists (plan 3.3). | FIXED: deleted. |
| B | minor | `ground_truth.stop_rule` | Literature and drug check required before assessment; `max_additional_actions: 0` (plan 3.4). | FIXED: labs, RNS, mediastinal CT; `max_additional_actions: 2`. |
| C | major | `ground_truth.assessment.required_recommendations` | Musts were diagnostic tests ("Confirm AChR...", "Perform RNS...", "Order CT chest...", "Document baseline FVC"); no thymectomy must despite AChR+ generalized MG at 60 without thymoma; no dose or steroid plan; dysphagia not addressed. | FIXED: pyridostigmine titration; low-dose prednisone escalation with monitoring, azathioprine after TPMT if steroids are long term; thymectomy referral per MGTX; respiratory escalation thresholds with IVIG or PLEX; speech and language swallow assessment; drug list counselling. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Seven template prohibitions incl. telithromycin (withdrawn) and the "pyridostigmine bridge" steroid rule (pyridostigmine does not prevent steroid worsening) (plan D). | FIXED: the three canonical prohibitions (steroid start, MG-worsening drugs, functional attribution before serology and neurophysiology). |
| E | minor | `ground_truth.avoided_actions[*]` | `[Wolfe_2016]` cited for EEG, CSF, MRI, echo, monitoring, PET (plan E). | FIXED: citations emptied; case rationale with Jacob 2025 in text. |
| C | minor | `ground_truth.differential` | MuSK MG entry relied on a MuSK result that is not indicated in an AChR-positive patient and is a subtype, not an alternative; thyroid eye disease said the ophthalmoplegia "resolves with cooling" (the ice pack acts on ptosis); LEMS features cited the deleted 50 Hz study. | FIXED: MuSK entry removed; TED and LEMS key features rewritten from the case data. |
| C | minor | `ground_truth.key_clinical_evidence[1,3,4,5]` | Levator excursion values, "CT chest mandatory", 50 Hz and telithromycin statements (plan E). | FIXED: MRD1 values, canonical mediastinal CT sentence with MGTX, post-exercise 7%, current drug list. |
| C | minor | `ground_truth.red_herrings[0].correct_interpretation` | Fatigability called "pathognomonic". | FIXED: "characteristic". |
| D | minor | `fallback_tool_outputs.ct.impression` | "does not address the question this patient's workup turns on" (plan F). | FIXED: plain normal head CT impression. |
| E | minor | `metadata.difficulty_rationale`, `last_revised`, `revision_reason` | Rationale counted literature and drug check as required tools. | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

The work-up now reads: AChR antibody with thyroid function (one initial report: AChR binding 8.7 nmol/L with elevated blocking 38% and modulating 62% antibodies, TSH 1.9, free T4 and anti-TPO normal; MuSK and LRP4 no longer reported because they are not indicated in an AChR-positive patient), RNS at 3 Hz (unchanged decrements 13/15/11% in trapezius, nasalis and anconeus; the 50 Hz study replaced by brief-exercise testing with a 7% increment), the ice pack test (now read on MRD1: left 1.0 to 3.5 mm), contrast mediastinal CT (no thymoma, fatty involution) and a respiratory baseline with weight-based values (FVC 2.85 L, 95% predicted, 40 mL/kg; MIP -66; MEP 84 cmH2O). Labs, RNS and CT are required; ice pack and respiratory recommended; literature and drug checks are no longer criteria. The exam now gives MRD1 and a left abduction (not adduction) deficit consistent with diplopia on leftward gaze, and no longer contains the NIF. Musts are management only: pyridostigmine titration, low-dose prednisone escalation with monitoring and azathioprine after TPMT if needed, thymectomy referral per MGTX (age 60, AChR-positive, no thymoma), respiratory escalation thresholds with IVIG or PLEX, swallow assessment, drug counselling. Prohibitions are the three canonical ones.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan CENTRAL 1: citation keys `[Jacob_2025]`, `[Evoli_2019]`, `[Lawn_2001]` used in text only until added to the MG pack.
- Plan CENTRAL 2: `icd_codes[0]` is G70.01 ("with acute exacerbation") in a stable new diagnosis; G70.00 fits. Not changed (ROUND_POLICY 3).
- Plan CENTRAL 3: synonyms accept "ocular myasthenia gravis" for this generalized case.

## Open questions for Andrea (judgment calls you could not settle)

- None. MGFA class IIa kept in the label: limb weakness and mild bulbar symptoms are both present, and IIa allows lesser oropharyngeal involvement.

## Verification

Adversarial check, 24 Oct 2026. Read the log, the full diff and the final case. Confirmed: serology in the initial labs (one Mayo-style laboratory, anti-TPO per the July 2026 guidance "thyroid function and thyroid antibodies in all patients"), no MuSK/LRP4/titin rows, NIF gone from the patient block, the left abduction deficit matching diplopia on leftward gaze in both exam fields, MRD1 values consistent between exam, ice pack report and expected evidence, BMI 26.4 and 40 mL/kg recomputed from 72 kg and 165 cm, 50 Hz study replaced by brief exercise, criteria/stop rule/prohibitions per plan 3.2-3.4, thymectomy must valid (60, AChR+, no thymoma), head CT and FDG_PET fallbacks carry clean wording and vocabulary values, leak guard passes. No reviewer notes exist for MG.

Found and fixed:
- C/B major: no SFEMG report was stored, so an SFEMG order (a common extra study, inside the allowance of 2) returned the library's normal SFEMG ("no evidence of a neuromuscular transmission defect"), contradicting the decrement and the AChR titre. Added a follow-up `request_emg_single_fiber` (left frontalis, mean MCD 64 microseconds, increased jitter 13/20, blocking 4/20), an optional criterion `action-single-fiber-emg` after RNS, and the two soft constraints of plan 3.3 (`RNS -> SFEMG`, `labs -> SFEMG`), matching the S01-S04 pattern.

Left as is: older template sentences with em dashes in `key_clinical_evidence[0,2]` and the red herring (pre-existing prose, correct content). perfect_agent passes (alternatives mediastinum_MRI and chest_CT answered by library normal reports, consistent with this normal CT); case_io check clean for this case.

## Condition audit (MG auditor, 24 Oct 2026)

- fallback_tool_outputs.echo.echo_type set to TTE. FIXED.
  Why: the discriminator guard (PATTERNS.md section 5) requires an exact vocabulary value on every case fallback; an empty echo_type answered every echo variant. The RS11-RS16 verifiers fixed this only in their own cases.
- initial_tool_outputs.body_imaging.region 'mediastinum' -> 'chest, anterior mediastinum' so the chest_CT alternative gets the case's own CT chest report (as S01-S04). FIXED.
  Why: perfect_agent warned that chest_CT fell back to a library normal report for this case.
- `perfect_agent.py` and `case_io.py check` re-run on all 30 MG cases after the changes; the hand-run discriminator guard reports 0 defects in the 30 MG cases.

## Close-out (24 Oct 2026)

- `ground_truth.diagnosis.icd_codes[0]` G70.01 -> G70.00. ICD-10-CM G70.01 is myasthenia gravis with (acute) exacerbation, including crisis; this is a new or stable presentation, not an exacerbation. G70.01 stays accepted as a secondary code (plans/MG-decisions.md, Q2).
- Synonyms (G70 entries rescoped): "ocular myasthenia gravis" removed (this is generalized MG); "generalized MG" and "generalised MG" added; bare "MG" retired (a one-token label matched any text mentioning MG).
- Result: accepted = ['myasthenia gravis', 'autoimmune myasthenia', 'generalized myasthenia gravis', 'generalised myasthenia gravis', 'generalized MG', 'generalised MG']; icd_codes = ['G70.00', 'G70.0', 'G70.01']. Applied with `apply_diagnosis_synonyms.py --prune --conditions myasthenia_gravis`; `--check` clean; perfect-agent and case guards pass.
