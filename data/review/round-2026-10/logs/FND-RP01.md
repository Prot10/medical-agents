# FND-RP01
Reviewer status: R1 none, R2 none (FND was never reviewed; no notes file) | Approved before this round: no

## Reviewer notes
No reviewer notes for this case.

| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | - |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | major | `ground_truth.action_criteria` | Template criteria (plan A): literature and drug check `recommended`, video-EEG `optional`, labels equal to rationales, "positive FND signs; AAN ..." and "FND criteria pack ..." citations. | FIXED: order exam (required), video-EEG (required), drug check (required), new optional `action-neuropsych-battery`, literature (optional, last); case-specific labels, rationales, expected evidence and citations. |
| A | major | `ground_truth.sequence_constraints`, `.stop_rule` | No constraint; stop rule only the exam. | FIXED: soft `action-4-analyze-eeg` before `action-2-check-drug-interactions` (taper rests on the recorded events, AAN 2025, Oto 2005); stop rule lists the three required criteria, `max_additional_actions` 0. |
| D | major | `followup_outputs[0]` (literature) | Misattributed source ("Espay ... Lancet Neurol 2018;17:84-98, new subtypes and shared mechanisms" is Hallett 2022), unverifiable figures and a prolactin row overclaiming specificity (plan B, fact 6). | FIXED: deleted; canonical `initial_tool_outputs.literature_search`. |
| C | major | `followup_outputs[1]` (drug check) | Plan-style output: switching to an SNRI, bridging with hydroxyzine, buspirone or gabapentin, vitamin D monitoring; carbamazepine with phenytoin, sertraline raising phenytoin, carbamazepine hyponatremia and sertraline with ibuprofen missing; sulfonamide allergy absent. | FIXED: deleted; `initial_tool_outputs.drug_interactions.general` lists the five medicines verbatim, the fact-16 pairs (mutual induction, sertraline raising phenytoin, inducers lowering sertraline and diazepam, additive hyponatremia, SSRI with NSAID), the allergy (no zonisamide), abrupt diazepam withdrawal; no dose or alternative. |
| C | major | `initial_tool_outputs.eeg.limitations` | Diazepam reduced from 20 mg to 5 mg a day within the 5-day monitoring after 26 years of use (withdrawal-seizure risk), contradicting the slow benzodiazepine taper the case requires. | FIXED: carbamazepine and phenytoin reduced during monitoring, diazepam continued at the usual dose. |
| B | minor | `initial_tool_outputs.eeg.findings[2]`, `.impression` | Bitemporal theta "identical to initial recording" (no initial recording exists) and "likely related to medications" (cause attribution); impression not in canonical form. | FIXED: theta described as brief drowsy runs without sharp component; canonical impression naming the five events, with the theta called nonspecific. Event types, locations and durations made explicit. |
| D | major | `initial_tool_outputs.clinical_assessment` | Meta keys in `criteria_met`; "Drug-refractory course" and history quotations counted as signs; scare-quoted 'seizures'; impression "...which is why video-EEG is required in this case rather than optional" (key leak). | FIXED: canonical shape with all library keys false (no sign, no event seen), findings for the examined systems, impression "No motor or sensory functional sign; neurological examination otherwise normal." |
| D | minor | `patient.neurological_exam.additional` | Commentary "The normal interictal examination in the context of 26 years of refractory 'seizures' ... is noteworthy." | FIXED: removed. |
| C | major | `ground_truth.assessment.required_recommendations` | Template musts (semiology must, video-EEG as a must, neuropsychology "recommended tier", duplicates, physiotherapy without a motor phenotype); no taper plan. | FIXED: M-DX, M-COMM, M-PSY (depression), M-RESCUE, M-ASM (carbamazepine and phenytoin one at a time, then diazepam slowly over weeks). |
| C | major | `ground_truth.assessment.prohibited_recommendations` | "per Stone 2018"; "start or continue" AEDs. | FIXED: P1, P2, P3, P5 with "or stop it abruptly", P6, P7. |
| C | major | `ground_truth.differential` | Epileptic seizures `high` after five events without ictal change; structural lesion cited an MRI not in the case; autoimmune encephalitis and malingering template rows. | FIXED: "Epileptic seizures (posttraumatic epilepsy)" `low` (canonical key feature, both types recorded during reduction); added "Hyperkinetic frontal lobe seizures" `low`, the mimic a neurologist weighs with bizarre motor events; template rows deleted. |
| B | major | `metadata.difficulty_description`, `.estimated_complexity`, `.red_herrings` | Named a "right anterior temporal encephalomalacia" MRI, a "mildly elevated GGT" and "low vitamin D", none of which exist in the case. | FIXED: rewritten from the case's real data (head injury, uncle, drowsy theta, 26-year label). |
| B | minor | `ground_truth.red_herrings` | Generic data points; "Stone 2018"; stressor-at-onset item without a stressor at onset. | FIXED: posttraumatic label, drowsy theta, paternal uncle, depression, each with the case's own data. |
| E | major | `ground_truth.key_clinical_evidence` | Template items with the "Interim composition decision" leak, OPTIONAL item and Stone 2018. | FIXED: 5 case-specific items. |
| C | minor | `ground_truth.avoided_actions[*]` | `[Stone_2018]`; generic rationales. | FIXED: `[Espay_2018]`/`[Stone_2016]`, patient-specific rationales; all kept as waste. |
| B | minor | `fallback_tool_outputs` | specialized_test `test_type: ''` with the "itself a harm" leak; advanced_imaging `modality: ''`; echo without `echo_type`. | FIXED: both nulled and removed from `metadata.fallback_tool_kinds`; echo `echo_type: TTE`. |
| E | minor | `metadata.difficulty_rationale`, `.revision_reason` | Templates. | FIXED: rewritten; `last_revised` 2026-10-24. |

## Changes, in one paragraph a physician can read before re-reviewing

The pathway is now the examination, the 5-day video-EEG (required) and the review of her antiseizure drugs and benzodiazepine (required, after the video-EEG by a soft constraint), with optional neuropsychology and literature last. The examination report records a normal interictal examination with no functional limb sign and no event seen, without commentary. The video-EEG impression names the five habitual events (three motor events with crying and spitting, two staring spells) without ictal change and calls the drowsy bitemporal theta nonspecific (no medication attribution); during monitoring carbamazepine and phenytoin were reduced and diazepam was continued, so the report no longer describes a rapid benzodiazepine taper. The drug check lists carbamazepine with phenytoin, sertraline raising phenytoin, the inducers lowering sertraline and diazepam, additive hyponatremia, sertraline with ibuprofen, the sulfonamide allergy (no zonisamide) and the risk of stopping diazepam abruptly. Musts: positive diagnosis of functional seizures from the recorded events, explanation to patient and family, psychological therapy with treatment of her depression, a written event plan without benzodiazepines, and withdrawal of carbamazepine and phenytoin one at a time and then diazepam over weeks. The differential is epileptic seizures and hyperkinetic frontal lobe seizures, both low. Metadata no longer names an MRI lesion and blood results that the case does not contain.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys per plan 1.1: `[Daum_2014]`, `[Stone_2016]`, `[Oto_2005]` (plan CENTRAL 1).
- EEG routing (plan CENTRAL 3): a `routine` EEG order receives the stored 5-day video-EEG.

## Open questions for Andrea (judgment calls you could not settle)

None open. Decisions taken:
- Plan 4 says "use the event-based impression" for RP01, but no event occurred during the examination (the exam is "entirely normal between episodes"). Writing an event-based impression would invent an observed event, so I used the plan's own no-sign impression (plan class H, "no limb sign and no event seen"); the semiology is in the HPI and in the video-EEG.
- The EEG limitations were changed to keep diazepam at the usual dose during monitoring; the original 75% reduction in 5 days after 26 years contradicts plan fact 9 and the case's own must.
- The plan gives RP01 no labs or MRI criterion; I added none.

## Verification

`perfect_agent.py FND-RP01 -v`: ok; the exam gets the clinical assessment, `eeg_type: video` gets the stored video-EEG, the drug check (after the EEG) gets `initial_tool_outputs.drug_interactions.general`. `case_io.py check FND-RP01`: schema and synonym guard OK; the only FND failures are the literature leaks of FND-P08 and S10 (other workers' cases). `test_case_guards.py -k FND-RP01`: 2 passed. No new dashes (the only one left is the hyphen in `diagnosis.accepted[0]`, not edited per ruling 3).
