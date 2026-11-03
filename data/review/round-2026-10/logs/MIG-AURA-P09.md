# MIG-AURA-P09
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for MIG-AURA) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. July 2026 tool guidance applied through the plan (structured ICHD-3 history required; MRA added as a separate study, class K). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `patient.clinical_history.family_history`, `patient.history_present_illness`, `patient.hpi`, `patient.chief_complaint` | The label says "familial intracranial aneurysm" but only the father had an aneurysm; familial aneurysm (and the screening indication) needs two or more affected first-degree relatives (plan P09). | FIXED: the sister (39) now has a 3 mm unruptured right posterior communicating artery aneurysm found on screening MRA last month; HPI, chief complaint and family history updated. Label unchanged. |
| A | major | `initial_tool_outputs.clinical_assessment` | Template (class A) assessment. | FIXED: attacks, aura type and evolution, duration, headache relation, ICHD-3 1.2.3 B (motor plus speech) and 1.2.3.2 sporadic (no affected relative), family history, vascular risk, examination, SNNOOP10 red flags (motor aura, two relatives with aneurysm); 5 of 6 criterion C characteristics. |
| D | major | `initial_tool_outputs.mri` | The brain MRI report carried the MRA finding (4 mm saccular left M1/M2 aneurysm) and a gadolinium mention (class K). | FIXED: non-contrast MRI with DWI and SWI, normal parenchyma, no haemorrhage, microbleed or vascular malformation; aneurysm text removed. |
| C | major | `ground_truth.action_criteria` (new `action-mra`), `followup_outputs[0]` | No vessel imaging criterion although the aneurysm is the core finding. | FIXED: required `order_advanced_imaging` `MR_angiography`; follow-up TOF MRA: 4 mm saccular left MCA bifurcation aneurysm, neck 3 mm, regular wall, no other aneurysm. Fallback `advanced_imaging` (normal MRA) set null and its kind removed. |
| D | major | `initial_tool_outputs.literature_search`, `followup_outputs` (three literature searches) | Template initial literature (guard leak); two empty follow-ups and one summary blob. | FIXED: initial null; one literature follow-up, last, with Thompson 2015 (AHA/ASA unruptured aneurysm guideline) and Greving 2014 (PHASES). |
| C | major | `followup_outputs` (drug check), `action-2` | `{"context": ...}` criterion (unreachable); output "search_aneurysm_triptan_interaction" stated triptans were avoided because of the aneurysm. | FIXED: stored check under `sumatriptan` in `initial_tool_outputs.drug_interactions` (served for any drug): triptans and ergots avoided because of hemiplegic migraine; no aneurysm-specific triptan data stated as such; propranolol with rizatriptan (5 mg), verapamil (avoid), topiramate, NSAIDs. Alternatives sumatriptan, rizatriptan, zolmitriptan, propranolol, verapamil, topiramate; required. |
| C | minor | `ground_truth.action_criteria` (`action-1`, `-3`, `-4`) | Literature required with an exact query; MRI pinned `contrast: false, protocol: stroke`; generic labels and rationales. | FIXED: literature optional `{}` last; MRI `{}` required; labels, evidence and rationales from the case. |
| A | minor | stop rule, sequence | Literature in the stop rule; no constraints. | FIXED: stop rule history, MRI, MRA, drug check, max 1; soft constraints history before MRI and MRI before MRA. |
| C | major | `ground_truth.assessment.required_recommendations` | A test must ("MRI/MRA required"); no BP target, no rupture warning, no neurovascular referral detail; nothing on the failed preventive. | FIXED: seven musts: explain hemiplegic migraine and the separate aneurysm; neurovascular MDT referral (PHASES 3, two relatives, MCA site); BP confirmed and treated below 130/80; remain a non-smoker, alcohol within limits, no stimulants; rupture warning symptoms; optimise prevention (propranolol up if pulse allows, or verapamil, lamotrigine, acetazolamide, never verapamil with propranolol); NSAID or paracetamol with antiemetic for attacks. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Ergot boilerplate; anticoagulation line without the reason. | FIXED: triptans and ergots in hemiplegic migraine; antiplatelet or anticoagulant for presumed TIA (with the aura features); verapamil added to propranolol. |
| C | major | `ground_truth.differential` | TIA `moderate` despite the stereotyped spreading aura and normal imaging (class F). | FIXED: TIA low, familial hemiplegic migraine low, symptomatic aneurysm or sentinel headache very low, vascular malformation very low, each with the excluding data. |
| E | minor | `ground_truth.key_clinical_evidence` | "July 2026 review" sentences (class D). | FIXED: rebuilt from the case data. |
| E | minor | `ground_truth.red_herrings` | Empty paths. | FIXED: father's SAH (family history) and the emergency department TIA label (HPI). |
| B | minor | `ground_truth.avoided_actions` | Echo cited `[Charles_2017]` (a migraine review, not an echo source); generic rationales. | FIXED: citation removed; CT, CSF, echo and monitoring rationales written for this case. |
| E | minor | `patient.history_present_illness`, `patient.hpi`, `patient.pmh[1]`, `patient.physical_exam.neurological`, `patient.clinical_history.medications[0].indication`, `metadata` | Em dashes; "occasional alcohol" against 6-8 units; `metadata.case_body_concerns` listed dropped ECG, EEG and labs. | FIXED: dashes replaced, alcohol made consistent; concerns cleared (none of those studies is indicated here); `condition_name` updated. The em dash in `accepted[0]` is left (field frozen). |

## Changes, in one paragraph a physician can read before re-reviewing

A 36-year-old man with five stereotyped attacks of right arm weakness and then word-finding difficulty building over 20-25 minutes, each followed by a left-sided migrainous headache, on propranolol 40 mg twice daily with two attacks on treatment. His father had an aneurysmal SAH 8 weeks ago, and the case now adds that his sister has an unruptured 3 mm aneurysm found on screening, so the label's "familial intracranial aneurysm" and the screening indication hold. The pathway: structured history (ICHD-3 1.2.3.2 sporadic hemiplegic migraine, red flags motor aura and familial aneurysm); brain MRI (normal; the aneurysm text has moved out); MR angiography (new, required: 4 mm unruptured saccular left MCA bifurcation aneurysm); drug check (required: triptans and ergots avoided because of hemiplegic migraine, verapamil not to be added to propranolol, rizatriptan 5 mg with propranolol); optional literature with AHA/ASA 2015 and PHASES. Musts: explain both diagnoses as separate; neurovascular referral; BP below 130/80; non-smoking, alcohol and stimulant advice; rupture warning signs; optimise the preventive; NSAID or paracetamol for attacks. TIA is now low in the differential.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys for Thompson BG et al., Stroke 2015;46:2368-2400 (AHA/ASA unruptured aneurysm) and Greving JP et al., Lancet Neurol 2014;13:59-66 (PHASES); cited by name until they exist.
- Guidance claims (plan 5.5): P09 gains MRA.

## Open questions for Andrea (judgment calls you could not settle)

- Familial definition: I added the sister's aneurysm (plan preference) instead of rewording the label, which is frozen. Confirm the added relative is acceptable.
- PHASES 3 (hypertension 1, size under 7 mm 0, MCA 2; age under 70, no earlier SAH, non-Finnish or Japanese population) is stated in a must; family history is not a PHASES item, so the MDT may lean to treatment rather than surveillance. The must leaves the choice to the MDT.

## Verification

Adversarial verifier, 24 Oct 2026. Read the log, the diff and the whole final case. No reviewer notes exist for MIG-AURA. Checked: the sister's aneurysm is added consistently to the chief complaint, HPI, family history, clinical assessment, MRA criterion and key evidence, so "familial" and the AHA/ASA 2015 screening indication (two or more affected relatives) now hold; the aneurysm appears only in the MRA report, not in the brain MRI; PHASES 3 is right (hypertension 1, MCA site 2, size under 7 mm, age under 70, non-Finnish/Japanese 0); ICHD-3 1.2.3 B (motor plus speech) and the 5 of 6 count agree with the history; laterality (right arm, left hemisphere aneurysm-unrelated, left headache) is consistent; the propranolol-rizatriptan (5 mg) and propranolol-verapamil statements are correct and agree with the musts and prohibitions; Thompson 2015 and Greving 2014 citations are real; the differential matches the final evidence.
Found: no error requiring a change. No edit made. perfect_agent and case_io check clean; leak guard passes.


## Close-out (24 Oct 2026)

Condition close-out (plans/MIG-AURA-decisions.md). Changes and reasons:

- citations [AAN_2000] -> [AHS_neuroimaging_2020] x1, [ICHD_3] x2.
- synonyms re-derived: the generic migraine-with-aura labels ("migraine with aura", "migraine with typical aura", "classic migraine", "migraine aura") and codes G43.1, G43.109, G43.119, G43.909 removed, because hemiplegic migraine is the subtype the case scores (triptan avoidance, genetics) and typical aura excludes motor aura; hemiplegic labels and G43.4, G43.419 kept.
- Citation [AAN_2000] retired: Silberstein 2000 covers treatment, not neuroimaging; imaging statements now cite Evans 2020 [AHS_neuroimaging_2020], test-waste statements [ICHD_3] (diagnosis is clinical).
Checks after the change: `perfect_agent.py` pass, `case_io.py check` clean for the case, `test_case_guards.py -k MIG-AURA-` 60/60.

## Discriminators and vocabulary (24 Oct 2026)

Wiring (`genetic_panel:hemiplegic_migraine`): new optional criterion `action-hm-genetic-panel` (adult sporadic HM; the case's work-up is the aneurysm). No stored output: the library's negative panel answers it.

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## Engineering text (25 Oct 2026)

Review-process wording (references to the round's rulings, the round policy file, the criteria packs, and tier markers such as "(optional)" in criterion labels and rationales) is shown to physicians in the review app, so it was rewritten in clinical language. The tier stays in the criterion's `importance` field; scoring is unchanged. `test_case_guards.py::test_no_review_process_text` now fails on any of it.

- criterion `action-hm-genetic-panel` label: "Optional: hemiplegic migraine gene panel (CACNA1A, ATP1A2, SCN1A, PRRT2)" -> "Hemiplegic migraine gene panel (CACNA1A, ATP1A2, SCN1A, PRRT2)"
- criterion `action-1-search-medical-literature` label: "Optional: literature on familial aneurysm screening and management of unruptured aneurysms" -> "Literature on familial aneurysm screening and management of unruptured aneurysms"

## Library contradictions (25 Oct 2026)

Case-specific reports stored where the benchmark library's normal report contradicted the case. Why: 4 mm saccular left MCA bifurcation aneurysm on the stored MRA; the library catheter angiogram reports no aneurysm.

- cerebral_angiography: ~4 mm saccular left MCA bifurcation aneurysm, no other lesion (fallback_tool_outputs.advanced_imaging)

Checks: `perfect_agent.py` pass; `test_case_guards.py -k MIG-AURA-P09` pass; no fixed order still answered by the library (`lib4.source`); no 60-character window of any criterion's expected_evidence in the added text; every criterion's served output unchanged (snapshot diff against the baseline).
