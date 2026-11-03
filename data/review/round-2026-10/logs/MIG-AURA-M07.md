# MIG-AURA-M07
Reviewer status: R1 none, R2 none (no reviewer notes for MIG-AURA) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. The physician input applied is the July 2026 tool guidance for `migraine_with_aura` (structured ICHD-3 history required; MRI only for red flags; CSF, ECG, EEG removed; labs optional; echo removed) and ROUND_POLICY. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | blocker | `ground_truth.diagnosis.accepted[0]` | "Exercise-triggered migraine with visual and confusional aura (ICHD-3 1.2.1); first episode" codes a single attack as 1.2.1 (ICHD-3 criterion A needs two attacks) and names "confusional aura", which is not an ICHD-3 aura type. The HPI says he never had an aura or significant headache before, so the story supports a single attack (plan 4, M07; plan 6 Q3 default). | FIXED: "Probable migraine with aura (ICHD-3 1.5.2), exercise-triggered visual aura; no structural cause". `icd_codes[0]` G43.109 unchanged. Synonyms after `accepted[0]` not touched (CENTRAL). |
| B | major | `initial_tool_outputs.clinical_assessment` | Template (class A): HPI sentences copied twice, generic SNNOOP10 line, placeholder modality score, "6 of 6" C characteristics and succession true although only one aura modality (visual) occurred. | FIXED: rewritten as a structured assessment of this patient: attack count 1, visual aura only, spread 20 min, resolution 30-35 min, confusion as accompanying feature with the brainstem symptoms checked and absent, headache timing, exam, named SNNOOP10 flags (first attack and exertional onset present, others absent), family history. `criteria_met`: A false, succession false, C 5 of 6, brainstem aura false, 1.2 false, 1.5.2 true. Impression: probable migraine with visual aura (1.5.2), no management or imaging content. |
| D | major | `initial_tool_outputs.mri` | Brain MRI impression reported "Normal MRA" (vessel study for free, class K) and a T1+Gd sequence while the criterion ordered `contrast: false`. | FIXED: MRA text removed; T1+Gd removed; sequences T1, T2, FLAIR, DWI/ADC, SWI; indication, technique and comparison stated; impression normal with no parieto-occipital FLAIR change. |
| C | major | `ground_truth.action_criteria` | No vessel study although the case's own key evidence and differential rely on MRA (RCVS, dissection) for a first exertional headache. | FIXED: new `action-mra` (recommended, `order_advanced_imaging` `MR_angiography`) with a normal head and neck MRA follow-up (no vasoconstriction, dissection, aneurysm or AVM). |
| D | major | `initial_tool_outputs.drug_interactions["general"]` | Guard leak: the summary was the criterion's expected text; content (pre-exercise indometacin, propranolol) unrelated to this case; empty interaction fields. | FIXED: replaced by a `sumatriptan` check against his ibuprofen and caffeine: no interaction, SmPC contraindications listed and none recorded, triptan at headache onset, NSAIDs during endurance exercise (AKI, hyponatraemia), caffeine and medication-overuse thresholds, propranolol and exercise capacity. |
| A | major | `action-2-check-drug-interactions` | Criterion used `{"context": ...}`, which no agent can send (class C); tier recommended with no concrete interaction. | FIXED: alternatives `{"drug": "sumatriptan"}`, `{"drug": "ibuprofen"}`, `{"drug": "naproxen"}`; tier optional (ROUND_POLICY 6: no interaction that changes management); label, evidence and rationale case-specific. |
| C | major | `followup_outputs` literature (3) | First output claimed "ICHD-3 recognises migraine with confusional aura" (false); second gave invented athlete advice (carbohydrate loading "prevents CSD") and patient-level prescribing; third concluded on this patient ("normal resting BP and normal MRI argues against this"). Unreferenced sources. | FIXED: all three deleted; one literature follow-up with real sources (ICHD-3 1.2, 1.5.2 and 4.2; Koppen and van Veldhoven, J Headache Pain 2013;14:99; Ducros, Lancet Neurol 2012;11:906-917), general evidence only, placed last. |
| A | major | `action-1-search-medical-literature` | Required literature step in the stop rule (ROUND_POLICY 5). | FIXED: optional, `required_arguments: {}`, last; removed from the stop rule. |
| C | major | `ground_truth.assessment.required_recommendations` | "Brain MRI/MRA required" must (test as must, class J); "Confirm ICHD-3 1.2 criteria" (wrong for one attack); "pre-exercise indometacin" (treatment of primary exercise headache, not migraine); "initiate preventive therapy if frequency rises" (vague). | FIXED: five musts: explain probable migraine with aura and graded return to running; acute plan at headache onset (ibuprofen or naproxen, or sumatriptan, antiemetic); no preventive after one attack, diary (AHS 2021, class P); hydration, fuelling, steady caffeine, no ibuprofen during long races; safety-net red flags. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Ergot prohibition with no ergot in the case (class I); "Do not assume RCVS without thunderclap and MRA evidence" is not a checkable prohibition. | FIXED: "Do not start migraine preventive medication after a single attack"; "Do not advise him to give up running". |
| C | major | `ground_truth.differential` | No brainstem-aura entry although the confusion raises it; no dissection entry; key features without the excluding results; focal seizure rationale ("aura duration too long") imprecise. | FIXED: brainstem aura (low, only one feature), RCVS (low, not thunderclap, MRA normal), cervical artery dissection (low, normal MRA), PRES (low, normotensive, no FLAIR change), TIA including paradoxical embolism (low, positive spreading symptoms, no infarct), focal occipital seizure (low, phenomenology). |
| B | major | `ground_truth.red_herrings` | Second entry with empty paths citing "A&E labs normal" (no labs in the case); third entry cites ECG, LVH 11 mm and Holter that do not exist (class E). | FIXED: ECG/LVH/Holter entry deleted; confusion entry re-pointed to `patient.history_present_illness` with an interpretation that uses only case data (no invented labs); headache entry interpretation updated (not thunderclap, normal MRA). |
| D | minor | `ground_truth.key_clinical_evidence` | Two engineering sentences ("Tier per the July 2026 clinical review...", "July 2026 review applied end to end...") (class D). | FIXED: deleted; four case pearls (attack-count rule, confusion is not an aura type, exertional red flag with ICHD-3 4.2 exclusions, normal MRI and MRA). |
| A | minor | citations | Duplicates (`"[ICHD_3]"` with `"ICHD_3"`, `"[AAN_2000]"` with `"AAN_2000"`) and free text "ICHD-3; NICE CG150 (2025)" (class N). | FIXED: one bracketed pack key per criterion; AHS 2020 named in the MRI rationale text (no key yet). |
| A | minor | order, constraints, stop rule | Literature first; no constraints; stop rule required literature with allowance 0. | FIXED: order history, MRI, MRA, drug check, literature; soft constraint history before MRI; stop rule `[action-3]`, allowance 1. |
| A | minor | `action-4-analyze-brain-mri.required_arguments` | `{"contrast": false, "protocol": "standard"}` misses an agent that asks for contrast or another protocol. | FIXED: `{}`; label and rationale case-specific (AHS 2020). |
| B | minor | `patient.hpi`, `patient.history_present_illness` | "takes no medications" while the list holds caffeine products and occasional ibuprofen. | FIXED: "takes no regular medications apart from caffeine around training and occasional ibuprofen". |
| A | minor | `fallback_tool_outputs` | Drug fallback "agent not specified", specialized-test fallback with empty `test_type` and an "incidental" finding, advanced-imaging fallback with empty modality (class M). | FIXED: set to null (library answers per value); `metadata.fallback_tool_kinds` reduced to csf and ct. CT and CSF fallbacks are correct normal reports and stay. |
| E | minor | `metadata.condition_name`, `difficulty_description`, `difficulty_rationale` | "Confusional aura", "avoid beta-blockers" and caffeine management framing no longer match the case. | FIXED: rewritten to the single-attack, probable migraine with aura framing. |

## Changes, in one paragraph a physician can read before re-reviewing
27-year-old male marathon runner with one attack, 4 weeks ago, during a half-marathon: a right-field zigzag visual aura spreading over 20 minutes with transient disorientation, resolving in 30-35 minutes, followed 20 minutes later by a 14-hour bilateral migrainous headache; normal examination. Because it is a single attack, the label is now probable migraine with aura (ICHD-3 1.5.2), and the structured assessment says so explicitly (criterion A not met, 5 of 6 C characteristics, confusion not an aura type, brainstem aura not met, first attack and exertional onset as red flags). The brain MRI no longer reports an MRA or a contrast sequence; MRA of the head and neck is a separate recommended study (normal) for RCVS and dissection exclusion. The drug check is optional and now checks sumatriptan against his ibuprofen and caffeine; the false "confusional aura" literature, invented athlete advice and indometacin plan are gone. Musts: explain the diagnosis and graded return to running, acute plan at headache onset, no preventive after one attack with a diary, trigger advice (hydration, steady caffeine, no ibuprofen during long races), safety-net. Red herrings and the differential use only data the case contains.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Label changed (plan 5.4): `accepted[0]` is now "Probable migraine with aura (ICHD-3 1.5.2) ...". The appended G43.109 synonyms still include "migraine with typical aura" (1.2.1, which a single attack does not meet) and "migraine aura" (token subset of "migraine without aura", plan 5.1). Add "probable migraine with aura" to the group and drop "migraine aura".
- Allow-list: `[AHS_neuroimaging_2020]`, `[AHS_2021]` (cited in text only here).
- Guidance claims: M07 gains MRA as a separate recommended study (plan 5.5).

## Open questions for Andrea (judgment calls you could not settle)
None. The relabel to 1.5.2 (plan 6 Q3) was decided by the HPI ("He had never had a visual aura before and no prior significant headaches").

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the diff and the whole final case against the plan (section 4 M07, classes A-Q) and ROUND_POLICY. No reviewer notes exist for MIG-AURA, so nothing was missing from the notes table. Checked: label relabel to 1.5.2 matches the HPI (single attack) and the structured fields (A false, C 5 of 6, succession false, 1.5.2 true); MRI report has no MRA or contrast sequence; MRA is a separate recommended criterion with its own follow-up; the drug criterion uses `{"drug": ...}` and is optional; literature optional and last, not in the stop rule; soft history-before-MRI constraint; red herrings point at real fields; no ergot or HRT boilerplate; no preventive must (class P); perfect-agent and leak guards pass.
Found and changed:
- `followup_outputs` literature `results[0].finding`: said primary exercise headache (ICHD-3 4.2) "has no aura", which is not an ICHD-3 statement. Now "is brought on by and occurs only during or after strenuous exercise".
- `ground_truth.differential` brainstem aura `key_features` said there was no reduced consciousness at all, while the red herring counts the disorientation as one brainstem-type feature. Reworded so both say: at most one brainstem feature (the disorientation, if counted), none of the others, so 1.2.2 is not met.
Re-ran `perfect_agent.py MIG-AURA-M07 -v` and `case_io.py check`: clean. Left as is: stale `metadata.case_body_concerns` text (metadata, not shown to the agent).

## Condition audit
Condition auditor, 24 Oct 2026 (uniformity pass over all 30 MIG-AURA cases).
- `metadata.case_body_concerns[0]`: stale authoring note "check_drug_interactions (only fallback)", untrue since the drug check now has its own stored output; removed, as P08, P09, RM11 and RS11 had already done (metadata only, not shown to the agent).

After the edit: `perfect_agent.py` 30/30, `case_io.py check` clean for the condition, `test_case_guards.py -k MIG-AURA` 60 passed.


## Close-out (24 Oct 2026)

Condition close-out (plans/MIG-AURA-decisions.md). Changes and reasons:

- citations [AAN_2000] -> [AHS_neuroimaging_2020] x2, [ICHD_3] x1, dropped x1.
- synonyms re-derived (`apply_diagnosis_synonyms.py --prune`): "migraine aura" removed (its tokens are a subset of "migraine without aura", a wrong answer); "migraine with aura", "migraine with typical aura", "classic migraine" and G43.1, G43.119, G43.909 kept.
- synonym "probable migraine with aura" added (ICHD-3 1.5.2 label).
- Citation [AAN_2000] retired: Silberstein 2000 covers treatment, not neuroimaging; imaging statements now cite Evans 2020 [AHS_neuroimaging_2020], test-waste statements [ICHD_3] (diagnosis is clinical).
Checks after the change: `perfect_agent.py` pass, `case_io.py check` clean for the case, `test_case_guards.py -k MIG-AURA-` 60/60.

## Engineering text (25 Oct 2026)

Review-process wording (references to the round's rulings, the round policy file, the criteria packs, and tier markers such as "(optional)" in criterion labels and rationales) is shown to physicians in the review app, so it was rewritten in clinical language. The tier stays in the criterion's `importance` field; scoring is unchanged. `test_case_guards.py::test_no_review_process_text` now fails on any of it.

- criterion `action-2-check-drug-interactions` rationale: "Optional: he takes no interacting drug and has no vascular contraindication, so the check does not change management." -> "He takes no interacting drug and has no vascular contraindication, so the check does not change management."
