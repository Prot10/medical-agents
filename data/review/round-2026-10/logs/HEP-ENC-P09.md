# HEP-ENC-P09
Reviewer status: R1 not reviewed, R2 approved | Approved before this round: yes

Changes are limited to real errors (plan section 4, P09 "real-error changes only", plus the errors listed under Own findings).

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 43f8f665-25a8-4a96-a335-24383a4eb220 | DECLINED (by design, ruling 4; plan C16) | Treatment is scored through the musts, never through a tool call; there is no treatment tool. The musts were checked against plan 1.2 and made specific: lactulose (MUST-LACT) with rifaximin continued, potassium and magnesium replacement with diuretics held (new must), acetaminophen "up to 2 g per day" without the incorrect condition "only after SDH stability confirmed", cultures before antibiotics, metformin held, transplant referral. The coagulopathy must (INR below 1.5, platelets above 100 before neurosurgery) is unchanged. |
| 7ed60ff7-bd34-4957-bd71-f498f6391d85 | FIXED | `ground_truth.assessment.required_recommendations[4]`: "3-4 soft stools" replaced by MUST-LACT (2-3 soft bowel movements per day, avoid over-titration; ACG 2026 rec 10, EASL 2022), with "Continue rifaximin 550 mg twice daily". The potassium 3.3 / magnesium 1.6 correction is a separate must (`required_recommendations[5]`). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `followup_outputs` (trigger `request_partial_he_treatment_response`) | Treatment-response panel (GCS 24 h, ammonia 74 to 58) delivered through `interpret_labs` (ruling 4, C1, C2). | FIXED: deleted. The partial response is already in the HPI as pre-encounter history; `red_herrings[0].field_path`/`location` now point to `patient.history_present_illness`. |
| D | major | `action-3-search-medical-literature`, literature follow-up | Required literature search whose output echoed the expected evidence (ruling 5, C4). | FIXED: criterion and follow-up deleted; removed from the stop rule. |
| C | major | `ground_truth.diagnosis.accepted[0]`, HPI, `past_medical_history[0]` | "Child-Pugh B, MELD 14" not derivable: bilirubin 2.4 (2), albumin 2.9 (2), INR 1.8 (2), mild ascites (2), HE grade II (2) = 10, class C; MELD 16, MELD-Na 18 (Na 134, Cr 1.0) (C10). | FIXED: `accepted[0]` "Child-Pugh C, MELD-Na 18" (em dash removed, "mandatory" dropped); history score dated "at her last hepatology review"; score pearl added. ICD codes unchanged. |
| C | major | `action_criteria` (new `action-diagnostic-paracentesis`), `followup_outputs[0]` | Mild ascites with encephalopathy and no diagnostic paracentesis (EASL 2018, AASLD 2021; C6). | FIXED: required criterion `order_microbiology {"specimen": "ascitic_fluid"}`; new follow-up `request_diagnostic_paracentesis` (PMN 64 cells/mm3, SAAG 2.2, protein 1.2 g/dL, Gram stain negative, no growth at 48 h); in the stop rule. |
| B | major | `followup_outputs` urine block, `initial_tool_outputs.labs.panels.Urinalysis` | The label's precipitant is a UTI, yet the urine culture returned "No growth", while the admission urinalysis panel carried "Pending (24-48h), E. coli growth anticipated" (culture result in the labs; contradictory blocks; C7). | FIXED: culture line removed from the labs; urine block now pyuria with >100,000 CFU/mL E. coli at 48 h, ampicillin-resistant, susceptible to nitrofurantoin, TMP-SMX, ceftriaxone and ciprofloxacin (agrees with the must "nitrofurantoin or TMP-SMX per susceptibilities"). |
| B | minor | `initial_tool_outputs.microbiology` | "No growth reported at the time of this encounter" / "No organism isolated to date" template (C7). | FIXED: one time point, "no growth at 48 hours (two sets)", tests `["culture"]`. |
| A | minor | `action-7`, `action-8-order-microbiology` | `before_antimicrobials` and `tests` arguments made three tests mandatory; label-only rationales (C7, C17). | FIXED: arguments reduced to the specimen; required labels per C7 (UTI in the label); case-specific expected evidence. |
| C | major | `patient.history_present_illness` | "IV lactulose" (lactulose is not given intravenously) and "empiric measures" (ambiguous; with the deleted F1 it implied antibiotics before the cultures the case scores as pre-antibiotic). | FIXED: "her lactulose was increased and given by nasogastric tube"; antibiotics not mentioned, so the cultures are pre-antibiotic; the HPI states that the exam is the 24-hour repeat examination. |
| B | major | `patient.neurological_exam.mental_status` | Exam gave GCS 13 (E3V4M6), disoriented to time and place, while the HPI (and the deleted 24-h panel) placed this encounter at GCS 14, oriented to place and person; "disoriented to place" is the West Haven grade III criterion against a grade II label. | FIXED: "GCS 14 (E4V4M6). Disoriented to time; oriented to place and person." |
| B | minor | HPI, `neurological_exam.cranial_nerves` | Headache was right-temporal while the chronic SDH is left-sided, yet the case uses the "unilateral headache" as a localising sign. | FIXED: left-temporal (ipsilateral to the SDH); key evidence [1] states it. |
| D | minor | `neurological_exam.additional` | "No SBP tenderness" and "likely UTI" (interpretation in the exam). | FIXED: "No abdominal tenderness. Dysuria reported on review of systems." |
| C | minor | `action-2-order-ct-scan` label/rationale | "Mandatory ... in any cirrhotic with encephalopathy" contradicts ACG 2026 rec 6 (imaging not routine). | FIXED: label "Non-contrast CT head"; rationale names the actual triggers (new focal deficit, unilateral headache, recent fall on coagulopathy). CT stays required. |
| B | minor | `initial_tool_outputs.labs` | Template TSH 2.1 and zinc 82; no CRP; criterion listed lactate but the report had none; summary incomplete (C9). | FIXED: TSH 1.8, zinc 63, CRP 34 mg/L (H), lactate 1.6 mmol/L; summary and interpretation list every flagged value. |
| A | minor | `action-1-interpret-labs` | Criterion demanded 10 named panels (C9). | FIXED: two alternatives `[CBC, CMP, coagulation, ammonia, urinalysis]` / `[CBC, BMP, LFTs, coagulation, ammonia, urinalysis]`; canonical label plus urinalysis; case expected evidence. |
| C | minor | `followup_outputs` DI (`request_drug_interaction_he_sdh`) | Metformin "current renal function adequate ... hold if risk increases" in acute decompensated (Child-Pugh C) cirrhosis with infection. | FIXED: metformin held (lactic acidosis risk), glucose monitored with insulin if needed; must added; acetaminophen written "up to 2 g per day". DI stays required (antibiotic with spironolactone, antithrombotics with SDH, metformin). |
| C | minor | `ground_truth.assessment.required_recommendations` | No transplant referral although the corrected class is C with recurrent overt HE (plan C10: update musts that depend on the class); no culture timing must. | FIXED: MUST-TX (MELD-Na 18, 14 months abstinent) and the C7 culture must added. |
| C | major | `ground_truth.differential` | SDH "primary cause" high; "HE alone" and "septic encephalopathy" left moderate after the CT and labs; SBP entry said a tap "could be performed"; stroke and NCSE entries cited "fallback" outputs (C14). | FIXED: SDH concurrent contributor (moderate); HE alone low (CT shows SDH); septic encephalopathy low (not septic, lactate 1.6, sterile blood cultures); SBP low (PMN 64); stroke and NCSE key features rewritten without engineering terms. |
| E | minor | `ground_truth.key_clinical_evidence` | Engineering text ("the pack's required ... step", "listed in the HE-ENC criteria pack", "Do not mark CT head or LP as harmful", a non-existent "hard constraint"); temperature 37.8 called fever. | FIXED: rewritten clinically; LP pearl states why LP is not indicated; score pearl and K-AMM added. |
| B | minor | `fallback_tool_outputs.eeg` | Normal EEG (PDR 9-10 Hz) in grade II HE, against `metadata.fallback_tool_kinds.eeg = abnormal_nonspecific` and the differential's EEG statement. | FIXED: diffuse theta-delta slowing with mild left voltage attenuation, no epileptiform discharges. |
| A | minor | `fallback_tool_outputs.mri.findings` | Empty findings (C8). | FIXED: SDH and atrophy findings. |
| C | minor | `fallback_tool_outputs.ecg` | QTc 438 ms in a woman called "mildly prolonged". | FIXED: "within normal limits". |
| E | minor | `metadata.difficulty_rationale` | Described the deleted literature step and consults. | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

The case design is unchanged: HE grade II precipitated by an E. coli UTI, with a concurrent chronic left SDH found on the CT that the right-sided signs require. The encounter is now explicitly the 24-hour re-examination: the HPI says lactulose was increased by nasogastric tube (not "IV lactulose") and the exam reads GCS 14, disoriented to time only, so it supports grade II; the headache is left-temporal, on the side of the SDH. The 24-hour treatment-response panel and the literature search are deleted. The label now reads Child-Pugh C (10 points), MELD-Na 18; the MELD 14 in the history is dated as the last clinic review. A diagnostic paracentesis is required (mild ascites; PMN 64, no SBP). The urine culture now grows E. coli (it previously returned no growth in a UTI case) and the culture line was removed from the admission urinalysis; blood cultures report no growth at 48 hours. Labs gain CRP 34 and lactate 1.6, and the template TSH and zinc values were replaced. Musts: lactulose to 2-3 soft stools with rifaximin continued, potassium to 4.0 or more and magnesium with diuretics held, acetaminophen up to 2 g per day, cultures before antibiotics, metformin held, transplant referral; the CT, neurosurgery, UTI treatment and coagulopathy musts are unchanged. The differential is updated after the work-up (SDH as a concurrent contributor, HE alone, septic encephalopathy and SBP low). Fallback EEG now shows diffuse slowing.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys per plan 1.1: `[ACG_HE_2026]`, `[EASL_HE_2022]`, `[EASL_decomp_2018]`, `[AASLD_ascites_2021]`.
- `accepted[0]` changed under ruling 3 (C10 scores, plan CENTRAL 6); ICD codes and synonyms unchanged.

## Open questions for Andrea (judgment calls you could not settle)

- Criterion order keeps the CT second (labs, CT, blood cultures, paracentesis, urine, drug check) rather than the plan's generic position 5: in this case the new focal signs make the CT the urgent step, and the reviewer approved that order.
- The encounter is set at 24 hours after admission with no antibiotic yet given, so that cultures can be pre-antibiotic as the policy scores them; the alternative (antibiotics started in the ED) would make the culture criteria impossible. Confirm this timeline is acceptable.
- The paracentesis of mild ascites is required per plan C6 and Q6.
- New values (PMN 64, SAAG 2.2, CRP 34, lactate 1.6, TSH 1.8, zinc 63, the E. coli susceptibilities) are invented to fit the case.

## Verification

Adversarial verification, 23 Oct 2026 (approved case: checked for churn as well as errors).

- Notes: both note ids are in the table. 7ed60ff7 is fixed (MUST-LACT 2-3 stools; no "3-4" anywhere in the case). 43f8f665 DECLINED by design is sound (ruling 4); the musts are specific and agree with plan 1.2.
- Scores recomputed from the printed values: MELD 16.3 -> 16, MELD-Na 18.4 -> 18 (Cr 1.0, bilirubin 2.4, INR 1.8, Na 134); Child-Pugh 10 = C (mild ascites 2, grade II 2). Label, key evidence and MUST-TX agree; the prior "Child-Pugh B, MELD 14" is dated in HPI and history.
- Grade II now supported by the exam (GCS 14, disoriented to time only); laterality consistent (left SDH on CT and MRI fallback, left-temporal headache, right-sided signs, left EEG attenuation in the fallback).
- Cross-field: urine culture positive in the only urine block, culture line gone from the admission urinalysis, blood cultures sterile, ascitic PMN 64 below 250 and SBP low; susceptibilities support the nitrofurantoin/TMP-SMX must; no avoided action matches a kept criterion; no "2-4", serial ammonia, literature output or engineering text left; edited prose keeps only pre-existing em dashes.
- The prose changes in this approved case (HPI timeline, exam, headache side) each correct a real inconsistency logged above; I found no gratuitous churn.
- Not changed, noted: the fallback CSF interpretation calls a protein of 44 mg/dL "mildly elevated" (pre-existing, fallback only, approved case). The worker's open question on the 24-hour timeline (no antibiotic yet, so cultures are pre-antibiotic) stands for Andrea.
- Changes made: none. `perfect_agent.py HEP-ENC-P09 -v` passes; `case_io.py check` clean for the case.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
"hepatic coma" (grade IV only) and the coma/no-coma code of the other grade are no longer granted at category level; K76.82 stays as the generic code.
- labels removed: "hepatic coma"
- codes removed: K72.91
- `case_io.py validate` OK; `perfect_agent.py` passes.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality '', impression 'No abnormality identified.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
