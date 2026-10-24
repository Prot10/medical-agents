# MIG-AURA-RS11
Reviewer status: no reviewer notes for MIG-AURA (R1 and R2 never reviewed this condition) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. The physician input is the July 2026 tool guidance for migraine_with_aura (structured history required; MRI for red flags; CSF, ECG, EEG removed; echo not routine), applied below. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | minor | `patient.history_present_illness`, `patient.hpi` | First attack treated with "loxoprofen" while the medication list names meloxicam (plan RS11). | FIXED: "treated with meloxicam". |
| B | major | `patient.history_present_illness`, `patient.hpi` | Second attack: "tense feeling on the left side of his mouth" with right arm and leg weakness (laterality flip; first attack had right face). | FIXED: "right side of his mouth". |
| B | major | `patient.neurological_exam.cranial_nerves`, `.sensory`, `patient.physical_exam.neurological` | Residual "decreased pain sensation in the left frontal region" contradicts the HPI ("fully neurologically intact"), is ipsilateral to the affected hemisphere (cannot come from a left-hemisphere aura) and would make the aura not fully reversible. | FIXED: facial and limb sensation intact. |
| B | minor | `patient.physical_exam.general` | "Mild residual left parietal headache" contradicts the HPI ("now headache-free"). | FIXED: "headache-free today". |
| B | major | `initial_tool_outputs.clinical_assessment` (class A) | Template: HPI sentences copied, generic SNNOOP10 line, placeholder modality score, "6 of 6" criterion C while succession is not described and the second attack's sensory symptom lasted hours. | FIXED: rewritten per element (attack count, motor and sensory aura, spread 20-25 min, no succession, durations, laterality, positive dysaesthesia, headache timing, consciousness, family history, exam, named red flags); criteria_met: succession false, duration false, 1.2 C 4 of 6, 1.2.3 C 3 of 4, sporadic criterion added; impression states 1.2.3 (sporadic 1.2.3.2) and the red flags, no management. |
| D | major | `initial_tool_outputs.literature_search` (class B) | Template block whose finding and summary equal the literature criterion's expected evidence (guard failure). | FIXED: deleted (null); the library answers. |
| D | minor | `followup_outputs[0]` (old) | Empty literature follow-up (`query: ""`). | FIXED: deleted. |
| D | major | `initial_tool_outputs.mri` (class K) | Brain MRI report gave MRA findings ("normal circle of Willis on MRA", "no carotid dissection"): vessel study for free. | FIXED: MRA text removed; T2 and SWI added to the normal finding; impression "Normal MRI brain. No acute or chronic infarct, haemorrhage or structural lesion." |
| C | major | `ground_truth.action_criteria` (class K) | No vessel study although dissection is in the differential and the key evidence claims "MRI/MRA". | FIXED: new `action-mra` recommended (`order_advanced_imaging {"modality": "MR_angiography"}`) with `followup_outputs[0]` normal intracranial and cervical MRA (no dissection, stenosis, aneurysm or malformation). |
| C | major | `ground_truth.action_criteria[action-4]` | MRI optional with `{"contrast": false, "protocol": "standard"}` despite motor aura with impaired consciousness (red flags). | FIXED: recommended, `required_arguments: {}`, label and rationale cite AHS 2020 and the DWI/TIA fact. |
| A | major | `ground_truth.action_criteria[action-2]` (class C) | Drug criterion used `{"context": ...}`, which no agent can send. | FIXED: `{"drug": ...}` alternatives sumatriptan, rizatriptan, zolmitriptan, triptan, ergotamine, lomerizine, meloxicam; tier required (triptan label exclusion changes the acute plan, ROUND_POLICY 6); label, rationale and expected evidence rewritten. |
| C | major | `followup_outputs[1].output` (drug, class C) | Summary-only block with empty interactions, contraindications and warnings, "theoretical" caution wording, duplicated sentence. | FIXED: interactions for lomerizine, meloxicam, diazepam; contraindications (triptan labels exclude hemiplegic and basilar-type migraine; ergots); warnings (unknown herbal medicine: ephedra, liquorice; metoclopramide limits); alternatives NSAID plus antiemetic, gepants or lasmiditan with limited data; sources cited; trigger includes triptan names. |
| A | minor | `ground_truth.action_criteria[action-1]` (rule 5) | Literature criterion required, template query, in the stop rule. | FIXED: optional, `{}`, moved last, out of the stop rule. |
| A | minor | `ground_truth.action_criteria[*].citations` (class N) | Duplicates ("[ICHD_3]" and "ICHD_3") and free text "ICHD-3; NICE CG150 (2025)"; `[AAN_2000]` on the drug check. | FIXED: one key per source; drug check cites its sources in the rationale text. |
| A | minor | `ground_truth.action_criteria` order, `sequence_constraints`, `stop_rule` | Literature first; no constraints; stop rule listed literature, max 0. | FIXED: order history, MRI, MRA, drug check, literature; soft constraint history before MRI; stop rule history and drug check, max 1. |
| C | major | `ground_truth.assessment.required_recommendations` (class J) | "Brain MRI/MRA required" must (a test, and contradicts the tier); generic acute line; preventive cited `[Holland_2012]` (NSAID guideline) for topiramate and verapamil and ignored his current lomerizine. | FIXED: musts are acute plan (one NSAID plus antiemetic with doses, no triptan or ergot), preventive review given two attacks on lomerizine (verapamil, flunarizine, acetazolamide, lamotrigine; topiramate alternative), genetics referral (CACNA1A, ATP1A2, SCN1A, PRRT2), emergency advice for an atypical attack. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` (classes G, I) | Ergot co-administration boilerplate (he takes no ergot); no TIA-anchoring prohibition although the chief complaint red herring is TIA. | FIXED: ergot line deleted; triptan/ergot prohibition kept; class G antiplatelet prohibition added, worded to this case's features (see Open questions). |
| C | major | `ground_truth.differential` (classes E, F) | TIA left moderate; MELAS excluded by a "normal lactate" that does not exist; seizure and syncope raised by the red herring not handled. | FIXED: TIA low with clinical features and imaging; FHM low; dissection low (MRA); focal seizure with Todd paresis low with reasons; cardiac syncope very low (added, raised by the red herring); MELAS very low without the lactate claim. |
| D | minor | `ground_truth.key_clinical_evidence` (class D) | Two "July 2026 review" engineering lines; "TIA exclusion via MRI/MRA is mandatory"; "triptans contraindicated". | FIXED: engineering lines deleted; four case-specific statements (ICHD-3 1.2.3 sporadic; imaging red flags and DWI fact; consciousness; triptan label). |
| E | minor | `ground_truth.red_herrings[1]` (class E) | Empty `location` and `field_path`; cites a normal EEG and Holter that the case does not contain. | FIXED: points to `patient.history_present_illness` (found unresponsive); interpretation without EEG or Holter. |
| B | minor | `ground_truth.red_herrings[0].correct_interpretation` | "after TIA is excluded by normal MRI/MRA" restated the DWI-excludes-TIA error. | FIXED: clinical features plus "imaging shows no infarct or arterial lesion". |
| C | minor | `ground_truth.avoided_actions[avoid-waste-3]` (class N) | PFO rationale cited `[Charles_2017]` (pathophysiology). | FIXED: citation removed; rationale names MIST, PRIMA, PREMIUM. |
| A | minor | `fallback_tool_outputs.specialized_test` (class M) | Junk fallback keyed "general_laboratory_panel". | FIXED: null. |
| B | minor | `metadata.difficulty_description`, `.difficulty_rationale` | Claimed normal DWI, EEG and lactate "confirm" the diagnosis (no EEG or lactate in the case). | FIXED: rewritten to the case content. |

## Changes, in one paragraph a physician can read before re-reviewing

This 39-year-old man with two attacks of right arm and leg weakness and right facial and perioral dysaesthesia, building up over 20-25 min and followed by left occipital headache, the second with transient unresponsiveness, now reads consistently: the mouth symptom is right-sided, the examination today is normal (the residual left frontal hypoaesthesia and residual headache that contradicted the HPI are gone) and the NSAID is meloxicam throughout. The structured history output applies ICHD-3 1.2.3 explicitly (two attacks, motor plus sensory aura, spread, unilateral, headache; no succession; the second attack's sensory symptom exceeded 60 min), records the sporadic criterion and names the red flags present (motor aura, impaired consciousness, new aura type). The work-up is history (required), brain MRI (recommended, any protocol; report now brain only), a new MR angiography of the head and neck (recommended, normal, excludes dissection), the drug check (required, any triptan, ergot, lomerizine or meloxicam call; real content: triptan labels exclude hemiplegic migraine, no interaction among his medicines, herbal product warning) and an optional literature search; the template literature block and the empty literature follow-up are gone. Musts: one NSAID plus antiemetic at headache onset without triptan or ergot, preventive review because two attacks occurred on lomerizine (verapamil, flunarizine, acetazolamide, lamotrigine, or topiramate), genetics referral for CACNA1A/ATP1A2/SCN1A/PRRT2, and emergency advice for an atypical attack; prohibitions: triptans and ergots, and antithrombotics for presumed TIA. The differential is graded at assessment time (TIA, FHM, dissection, seizure low; syncope and MELAS very low).

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Vocabulary `genetic_panel:hemiplegic_migraine` (CACNA1A, ATP1A2, SCN1A, PRRT2): until it exists the gene test is a referral must here (plan section 5.2).
- Synonyms: G43.109 group "migraine aura" credits wrong diagnoses (plan section 5.1); appended to this case's accepted list.
- Guidance claims: RS11 gains MRA as a separate study (plan section 5.5).
- Citation keys used only in rationale text until added: AHS 2021 (Ailani 2021), AHS neuroimaging 2020 (Evans 2020), MIST/PRIMA/PREMIUM.

## Open questions for Andrea (judgment calls you could not settle)

- Decided: the class G canonical prohibition names "succession of symptoms" and "positive symptoms spreading", but in this case motor and sensory symptoms began together. I kept the canonical structure and filled it with this case's actual features ("motor and sensory symptoms spreading over 20-25 minutes, followed by headache, in two stereotyped attacks") so the prohibition does not contradict the structured history.
- Decided: residual left frontal hypoaesthesia removed rather than kept as a finding, because it contradicted the HPI and cannot arise from a left-hemisphere aura; if the source report (PMC11348355) records it as a genuine residual sign, it would argue against a fully reversible aura and the case would need a different label. Nothing for Andrea to supply unless the source says otherwise.

## Verification
Adversarial verifier, 24 Oct 2026. Read the whole final case, the original patient block, the clinical assessment and the assessment section from `git show HEAD`, and the follow-up matcher (`tools/followup_matcher.py`).
- Checked: every own finding in the log against the file (meloxicam throughout, right-sided mouth symptom in both HPI fields, exam sensation intact, headache-free, MRA text gone from the brain MRI report, `action-mra` with its follow-up, `{"drug": ...}` alternatives, literature optional and last, stop rule history plus drug check with max 1, ergot boilerplate gone, `[Charles_2017]` gone). All hold.
- ICHD-3 arithmetic: 1.2.3 C is 3 of 4 (spread, unilateral, headache; duration false because the sensory symptom of attack 2 outlasted 60 min) and 1.2 C is 4 of 6; structured fields agree with the narrative. Sequence constraint direction verified against the schema (`before_criterion_id` = history). A drug call with lomerizine or meloxicam (not in the trigger tokens) still reaches the stored output because the case has no initial drug output (matcher precedence 2).
- Found and changed: (1) the structured history said the headache was "relieved by an NSAID" for both attacks; the HPI records relief only for attack 1 (meloxicam): now "the first relieved by meloxicam". (2) `metadata.case_body_concerns` still listed `order_advanced_imaging` as a dropped useless tool although it is now the `action-mra` criterion: removed from the list. (3) `metadata.fallback_tool_kinds.specialized_test` described the fallback the worker set to null: key removed.
- Not changed: the must "Do not use a triptan or ergot derivative..." overlaps the prohibition but does not contradict it. The worker's removal of the residual left frontal hypoaesthesia is sound (it contradicted "fully neurologically intact" and is ipsilateral to the affected hemisphere).
- Checks after the edits: `perfect_agent.py -v` ok; `case_io.py check` schema and synonym guard ok, no failure names this case; `test_case_guards.py -k MIG-AURA-RS11` passes.


## Close-out (24 Oct 2026)

Condition close-out (plans/MIG-AURA-decisions.md). Changes and reasons:

- citations [AAN_2000] -> [AHS_neuroimaging_2020] x1, [ICHD_3] x1.
- synonyms re-derived: the generic migraine-with-aura labels ("migraine with aura", "migraine with typical aura", "classic migraine", "migraine aura") and codes G43.1, G43.109, G43.119, G43.909 removed, because hemiplegic migraine is the subtype the case scores (triptan avoidance, genetics) and typical aura excludes motor aura; hemiplegic labels and G43.4, G43.419 kept.
- Citation [AAN_2000] retired: Silberstein 2000 covers treatment, not neuroimaging; imaging statements now cite Evans 2020 [AHS_neuroimaging_2020], test-waste statements [ICHD_3] (diagnosis is clinical).
Checks after the change: `perfect_agent.py` pass, `case_io.py check` clean for the case, `test_case_guards.py -k MIG-AURA-` 60/60.

## Discriminators and vocabulary (24 Oct 2026)

Wiring (`genetic_panel:hemiplegic_migraine`): new optional criterion `action-hm-genetic-panel` (adult-onset sporadic HM, two attacks: low yield, no change to management). No stored output: the library's negative panel answers it, consistent with the sporadic label. The referral must stays.

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.
