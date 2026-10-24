# VASC-DEM-P04
Reviewer status: R1 none, R2 none (VASC-DEM has no notes file; never reviewed) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer note exists for this case or condition. All changes below come from the condition plan (classes C1-C19) and from my own audit. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | blocker | `ground_truth.action_criteria[action-4-analyze-brain-mri].alternatives` | Plan C1: non-schema `sequences` key plus `protocol`/`contrast`; no real call could match the required MRI. | FIXED: `analyze_brain_mri {}`; label, rationale, expected evidence rewritten. |
| D | major | `initial_tool_outputs.literature_search`, `fallback_tool_outputs.literature_search`, criterion `action-6-search-medical-literature` | Plan C2: output repeated the criterion's expected evidence (leak test failed). | FIXED: criterion deleted, initial null, fallback deleted. |
| B | major | criterion `action-7-check-drug-interactions`, `initial_tool_outputs.drug_interactions`, `fallback_tool_outputs.drug_interactions` | Plan C3 group O: generic criterion and a generic "no prohibitive interaction" fallback; no case content although the case turns on apixaban. | FIXED: criterion kept optional `{}` with new label, rationale and evidence; fallback deleted; initial output keyed `apixaban` with case content in pharmacology voice (no interaction with bisoprolol, ramipril, atorvastatin; antiplatelet, NSAID and SSRI bleeding interactions; dose-reduction criteria; ICH as the most serious bleeding complication; LAAO as the non-pharmacological alternative). Wording checked against the expected evidence (leak test passes). |
| B | major | `patient.physical_exam` | Plan C19: dose check impossible without a weight (Vitals has no weight field). | FIXED: `physical_exam.general` "Weight 57.7 kg, height 158 cm" (BMI 23.1 as in demographics). With age 81 the apixaban 2.5 mg twice-daily reduction meets two criteria; Cockcroft-Gault CrCl about 40 mL/min. |
| D | major | `patient.neurological_exam.mental_status` | Plan C4: MoCA total and item losses in the exam. | FIXED: bedside observation, "Formal cognitive screening reported separately". |
| C | major | `initial_tool_outputs.clinical_assessment` | MoCA arithmetic: listed losses plus month gave 11 points lost, i.e. 19 raw, but 12 years of education earns +1 (would be 20); "fluency 8 animals" is not the MoCA letter-fluency item; `criteria_met.haemorrhagic_lesion_as_substrate` is a cross-modality (MRI) conclusion; impression argued the chronic vascular process. | FIXED: abstraction 1/2 added so raw 18 + 1 education = 19/30 (total unchanged everywhere); fluency "8 words beginning with F"; the substrate flag removed; impression lists totals, losses, the hemianopia caveat, FAQ 19/30 and GDS 4/15 only. |
| D | major | `initial_tool_outputs.specialized_test.impression` | "informant-rated loss of instrumental independence" (threshold statement). | FIXED: profile statement with the oral-adaptation note and FAQ value. |
| D | major | `initial_tool_outputs.mri.impression`, `.additional_observations` | Plan C5: impression named the cognitive syndrome and the recurrence risk; observations argued against hypertensive arteriopathy, gave prognosis, called grade 2 CSO-PVS and posterior WMH Boston "supportive markers". | FIXED: numbered modality-only impression keeping the Boston v2.0 sentence; observations are pertinent negatives (no deep/infratentorial microbleed, no lacune, no acute haemorrhage, basal ganglia PVS not enlarged); "disseminated siderosis" label removed from the SWI signal text (extent stated as four sulci). |
| B | major | `initial_tool_outputs.labs` | Plan C6: Hct 41.6 with Hb 12.2; female HDL range ">40"; eGFR range ">60"; INR in CMP with `clinical_significance`; template values; interpretation "supports the reduced apixaban dose ... excluding reversible causes". | FIXED: Hct 36.8; HDL range ">50" with value 57 (50 would have sat on the limit); eGFR ">=60" (54 flagged); `Coagulation` panel PT 13.2 s, INR 1.1, aPTT 31 s; WBC 6.1, MCV 92, Na 140, K 4.4, ALT 15, albumin 3.9, folate 13.4; interpretation lists only the flagged eGFR and HbA1c. |
| B | major | `fallback_tool_outputs.cardiac_monitoring` | Holter fallback "Sinus rhythm throughout" in a patient with permanent AF and an irregularly irregular pulse. | FIXED: AF throughout, rate 51-112 (average 74), no pauses. |
| B | major | `fallback_tool_outputs.ecg` (absent) | The library ECG is a normal sinus report, contradicting permanent AF if a model orders an ECG. | FIXED: case ECG fallback: AF, rate 72, QRS 92 ms, QTc 438 ms, no acute ST-T change. |
| B | minor | `fallback_tool_outputs.echo` | Normal left atrium after 8 years of permanent AF; impression "No cardioembolic source identified". | FIXED: LA moderately dilated (LAVI 44 mL/m2); descriptive impression. |
| B | major | `fallback_tool_outputs.advanced_imaging`, `.labs`, `.ct` | Plan C7: off-pathway giveaways. | FIXED: advanced_imaging and labs fallbacks deleted; CT fallback rewritten for this patient (left occipital chronic cavity, posterior WM hypodensity, CT cannot show microbleeds or siderosis). `metadata.fallback_tool_kinds` updated. |
| B | minor | `followup_outputs` | Library CSF would return a normal Abeta42 (980 pg/mL) if an LP were ordered anyway. | FIXED: case CSF follow-up (Abeta42 240 and Abeta40 3900 pg/mL decreased, ratio 0.062, tau normal, RBC 3). |
| C | major | `ground_truth.avoided_actions[avoid-harm-1-analyze-csf]` | Plan C9: LP in chronic CAA is waste, not harm; rationale claimed CSF cannot separate vascular from parenchymal amyloid. | FIXED: severity `waste`, rationale per plan plus "an LP would also require interrupting apixaban". |
| C | minor | `ground_truth.avoided_actions[*].rationale` | Plan C18: generic and "already obtained" rationales; echo/monitoring rationale said "small-vessel burden". | FIXED: case-specific rationales (echo and monitoring: AF already documented, no ischaemic infarct, decision turns on CAA). |
| A | minor | `ground_truth.action_criteria[*]` | Plan C13: rationale equals label; duplicate unbracketed keys; generic expected evidence. | FIXED: case-specific rationales and evidence; bracketed keys only. Order per C16: screen, neuropsych, labs, MRI, drug check. |
| C | major | `ground_truth.assessment.required_recommendations` | Musts restated tool steps (obtain MRI, apply Boston, exclude hypertensive arteriopathy); "refer for a non-pharmacological alternative" unnamed; no BP target; no citations. | FIXED: six musts: diagnosis by Boston v2.0 with decline preceding the bleed; stop apixaban and avoid anticoagulation, noting the dose was correct [AHA_ASA_2022_ICH]; cardiology referral for LAAO (CHA2DS2-VA 3) [AHA_ASA_2022_ICH] [ESC_AF_2024]; BP below 130/80 (132/74 now) [AHA_ASA_2022_ICH]; answer the daughter and record the decision; falls and IADL support. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | LP prohibition partly wrong; "Do not leave the anticoagulation question unanswered a second time" is a must phrased as a prohibition. | FIXED: LP prohibition per plan; the unanswered-question item became the must above; antiplatelet item reworded (no em dash); hypertension-attribution item extended to "or to apixaban dosing". |
| C | major | `ground_truth.differential[0]`, `[1]` | Plan C8: hypertensive arteriopathy and "anticoagulation as the sole cause" left `moderate`. | FIXED: both `low` with key features from the MRI and the correct dose; subcortical ischaemic entry no longer calls posterior WMH a Boston marker. |
| B | minor | `ground_truth.key_clinical_evidence`, `.red_herrings[*].field_path` | Dash in KCE[3]; no evidence item on the dose; empty field paths. | FIXED: KCE[3] reworded, new KCE on the correct dose; field paths `past_medical_history[0]` and `[1]`. |
| B | minor | `ground_truth.stop_rule.max_additional_actions` | 0. | FIXED: 1; required set unchanged; soft screen-before-MRI constraint kept. |
| E | minor | `initial_tool_outputs.clinical_assessment.findings[*]` | Em dashes in untouched finding strings. | FLAGGED: left (plan: only in rewritten sentences). |
| - | check | plan 3.6 | perfect_agent.py ok; probes: drug check returns the apixaban output for any drug; ECG and Holter fallbacks show AF; CSF returns the case follow-up. `test_case_guards -k VASC-DEM-P04` 2 passed; `case_io.py check` no failure names P04; `sequences` count 0. | - |

## Changes, in one paragraph a physician can read before re-reviewing

Same patient and same answer: an 81-year-old woman with permanent AF who had a left occipital lobar haemorrhage on apixaban 14 months ago, was restarted on it, and has two years of decline that preceded the bleed; MRI shows seventeen strictly lobar microbleeds and disseminated cortical superficial siderosis, probable CAA by Boston v2.0. Her weight (57.7 kg) is now in the examination, so an agent can see that the 2.5 mg dose was correct and the bleed was not a dosing error. The exam no longer gives the MoCA; the MoCA arithmetic now works (raw 18 plus the education point gives 19/30; letter fluency, abstraction 1/2). Reports describe only their own findings; the MRI keeps its Boston statement. Labs: Hct matches Hb, female HDL range, INR in a coagulation panel, interpretation lists only eGFR 54 and HbA1c 5.7%. Off-pathway Holter and ECG now show AF instead of sinus rhythm. Literature step removed; the drug check is optional and returns a real apixaban review. LP is waste (a CAA-pattern CSF answers if ordered). Hypertensive arteriopathy and "apixaban alone" are low in the differential. Musts: stop apixaban and avoid anticoagulation, refer for LAAO, BP below 130/80, answer the daughter's question explicitly, falls and IADL support.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys used: `[AHA_ASA_2022_ICH]`, `[ESC_AF_2024]` (plan 5.4).
- Synonyms (plan 5.1): CAA labels and I68.0 for this case; `F06.7` should not be credited for a dementia-severity case.
- Schema: `Vitals` has no weight field, so the weight sits in `physical_exam.general`; a `weight_kg` vital would make DOAC and CrCl dosing checkable in every condition.

## Open questions for Andrea (judgment calls you could not settle)

- None.

## Verification

Adversarial check, 24 Oct 2026. Read the log, the diff and the final patient, ground truth, reports and follow-ups. Verified: weight 57.7 kg and height 158 cm give BMI 23.1 (matches demographics); two apixaban reduction criteria (age 81, weight 60 kg or less) so 2.5 mg twice daily was correct, Cockcroft-Gault about 39 mL/min; eGFR 54 matches creatinine 1.02 (CKD-EPI about 55); Hct 36.8 with Hb 12.2; female HDL range; MoCA arithmetic (12 points lost, raw 18 + 1 = 19/30) and exam orientation (month incorrect) agree; CSF follow-up ratio 240/3900 = 0.062 flagged low; left occipital haemorrhage and right hemianopia consistent across history, exam, MRI and CT fallback; AF consistent in ECG, Holter and echo fallbacks; CHA2DS2-VA 3 (age 75 or more, hypertension) correct; musts (stop apixaban, LAAO referral, BP target) agree with prohibitions (no anticoagulation, no antiplatelet substitute); drug-check output in pharmacology voice, leak guard passes.
Found: nothing that needed a change. perfect_agent.py pass; case_io.py check: schema OK, no failure names P04.

## Condition audit
Condition auditor, 24 Oct 2026. Scripted checks over all 30 VASC-DEM cases (plan classes C1-C21, PATTERNS.md, lab arithmetic) found the stragglers below in this case; changed through `case_io`.

| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | minor | `initial_tool_outputs.clinical_assessment.findings[Memory].performance` | Plan C5 (screen gives scores only): "— retrieval pattern" was an interpretive label left in the screen, removed in the other cases' screens. | FIXED: "2/5 unaided, 4/5 cued" (scores only; also removes the em dash). |
| D | major | `initial_tool_outputs.clinical_assessment.criteria_met` | Plan 1.2 and C5 (no report states the severity): the screen's structured fields still carried independence_in_iadl_lost, executive_predominant_profile, i.e. the mild-versus-major threshold, the profile verdict or history items. Workers removed these keys in the other 19 cases; here they survived (the P03 worker flagged the question for a condition-wide decision). | FIXED: keys removed; `criteria_met` keeps domain impairment and cue-responsive recall. The informant FAQ score stays in the report as an instrument score. |

perfect_agent.py, case_io.py check and test_case_guards re-run on all 30 VASC-DEM ids: clean.

## Close-out (24 Oct 2026)

Condition close-out per `plans/VASC-DEM-decisions.md`.

- Synonyms (diagnosis_synonyms.yaml, applied with `--prune --conditions vascular_dementia`): F06.7, I67.3 and the umbrella "vascular cognitive impairment" no longer accepted (mild-VCI answers must not score in a dementia case); subtype labels scoped by mechanism, here "cerebral amyloid angiopathy", "CAA" and I68.0. Generic labels "vascular dementia", "major vascular neurocognitive disorder", "major neurocognitive disorder due to vascular disease", "VaD"; codes F01.50, F01.51, F01.5, F01.9, F01.A0-C0.
- `action-3-interpret-labs`: RPR and HIV removed from `required_arguments.panels` and the label; `[AAN_dementia_2001]` added. AAN 2001: syphilis screening "is not justified unless clinical suspicion for neurosyphilis is present"; NICE NG97 does not test routinely; this case has no risk factor. The stored labs output keeps its RPR and HIV results, so an agent that orders them still receives them (decision Q1).
- `metadata.revision_reason`: the stale August literature/interaction audit text replaced by the round's (summary CENTRAL 9; not read by the harness).
- `metadata.fallback_tool_kinds`: cardiac_monitoring normal->case, ct normal->case, ecg normal->case, echo normal->case (the fallback describes this patient, not a library normal; summary CENTRAL 9).

Checks after the close-out: `perfect_agent.py` and `case_io.py check` clean for this case; `test_case_guards -k VASC-DEM-` clean; `apply_diagnosis_synonyms.py --check --conditions vascular_dementia` clean.
