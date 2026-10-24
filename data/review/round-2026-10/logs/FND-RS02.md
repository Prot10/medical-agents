# FND-RS02
Reviewer status: R1 none, R2 none (FND was never reviewed; no notes file) | Approved before this round: no

## Reviewer notes
No reviewer notes for this case.

| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | - |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | major | `ground_truth.action_criteria` | Template criteria (plan A): literature and drug check `recommended`, MRI and video-EEG `optional` with the shared "Consider MRI only for..." label, template citations. | FIXED: order exam (required), brain MRI `{contrast: false, protocol: standard}` (recommended, CNS vasculitis question), video-EEG (required), drug check (required), new optional `action-neuropsych-battery`, literature (optional, last); case-specific labels, rationales, expected evidence, citations. |
| A | major | `ground_truth.sequence_constraints`, `.stop_rule` | No constraints; stop rule only the exam. | FIXED: soft exam before MRI and soft video-EEG before drug check (plan 3.3); stop rule exam, video-EEG, drug check; `max_additional_actions` 0. |
| B | major | `initial_tool_outputs.eeg` | Impression named one captured event while the limitations said three; the only finding had empty morphology and frequency; impression not canonical, no final period. | FIXED: three event findings (the examination event, 70 s and 110 s), with the posterior alpha rhythm during the 2-minute motionless phase; canonical impression; limitations state the artifact. |
| C | major | `initial_tool_outputs.mri` | Gadolinium reported (`Post_contrast`) against a `contrast: false` criterion; "in the setting of hypertension and diabetes" (cross-field); impression a list of excluded diseases. | FIXED: non-contrast report (T1, T2/FLAIR, DWI/ADC, SWI), technique line, small vessel change described, impression "No acute intracranial abnormality..." with no disease list. |
| D | major | `initial_tool_outputs.clinical_assessment` | Meta keys in `criteria_met`; findings with the commentary "this pattern is not consistent with organic weakness"; observed event not reported; key-leak impression. | FIXED: canonical shape; 2 validated signs (collapsing weakness, distractibility); neuropathy signs reported separately; observed event with vital signs; event-based impression. |
| D | minor | `patient.neurological_exam.motor` | Interpretive clause "this pattern is not consistent with organic weakness". | FIXED: removed. |
| C | major | `followup_outputs[1]` (drug check) | Levetiracetam-only plan output claiming it "can be tapered relatively quickly given its short half-life and low withdrawal-seizure risk"; no gabapentin interaction, renal dosing or sulfonamide allergy. | FIXED: deleted; `initial_tool_outputs.drug_interactions.general` lists the four medicines verbatim, levetiracetam with gabapentin (additive sedation), mood effects, gradual withdrawal, renal dosing, the allergy (no zonisamide). |
| D | major | `followup_outputs[0]` (literature) | Hallett 2022 attributed to "Espay ... Lancet Neurol 2018"; "reduced episode frequency" claim (plan B, fact 10). | FIXED: deleted; canonical `initial_tool_outputs.literature_search`. |
| C | major | `ground_truth.assessment.required_recommendations` | Template musts; no levetiracetam taper; no plan for the stopped vasculitis treatment. | FIXED: M-DX, M-COMM, M-PHYSIO, M-PSY (health anxiety, grief, caregiver strain), M-RESCUE, M-ASM (levetiracetam only, gabapentin continued), rheumatology review of the vasculitis treatment. |
| C | major | `ground_truth.assessment.prohibited_recommendations` | "per Stone 2018"; "start or continue" AEDs. | FIXED: P1, P2, P3, P5 with "or stop it abruptly", P6, P7, and "Treat the events as CNS vasculitis with high-dose corticosteroids or cyclophosphamide". |
| C | major | `ground_truth.differential` | Epileptic seizures `moderate` after recorded events; structural, encephalitis and malingering template rows; CNS vasculitis, syncope (he reports palpitations) and the neuropathy question missing. | FIXED: epileptic seizures `low` (canonical), CNS vasculitis `low` (MRI), convulsive syncope or arrhythmia `low` (stable vitals during an observed event), diabetic neuropathy as the cause of the weakness `low`. |
| B | major | `ground_truth.red_herrings[0]` | "Family history of epilepsy" while the family history says "No family history of epilepsy". | FIXED: deleted; red herrings now the vasculitis with stopped methotrexate, the small vessel white matter change, palpitations with toe cyanosis, and the stressors. |
| E | major | `ground_truth.key_clinical_evidence` | Template items with the "Interim composition decision" leak, OPTIONAL item and Stone 2018. | FIXED: 5 case-specific items. |
| C | minor | `ground_truth.avoided_actions[*]` | `[Stone_2018]`; generic rationales. | FIXED: `[Espay_2018]`/`[Stone_2016]`, patient-specific rationales; all kept as waste. |
| B | minor | `fallback_tool_outputs` | specialized_test and advanced_imaging untyped with the leak sentence; echo without `echo_type`. | FIXED: nulled and removed from `fallback_tool_kinds`; echo `echo_type: TTE`. |
| E | minor | `metadata.difficulty_description`, `.difficulty_rationale` | "A systematic workup that excludes organic etiologies" (exclusion model); template rationale. | FIXED: rewritten; `last_revised` 2026-10-24. |

## Changes, in one paragraph a physician can read before re-reviewing

The pathway is the examination, one non-contrast brain MRI for the CNS vasculitis question (recommended, after the examination), the 48-hour video-EEG (required) and the levetiracetam review (required, after the video-EEG), with optional neuropsychology and literature last. The examination report counts collapsing weakness and distractibility, keeps the neuropathy signs apart, and describes the observed event (preserved awareness during bilateral shaking, a 2-minute motionless phase with recall, stable vital signs). The video-EEG now reports all three captured events, including normal posterior alpha during the motionless phase, where the old impression named one. The MRI is now a non-contrast report with small vessel change only. The drug check covers levetiracetam with gabapentin, mood effects, renal dosing, gradual withdrawal and the sulfonamide allergy. Musts: positive diagnosis, explanation, physiotherapy for the functional weakness and fear-avoidance, psychological therapy for health anxiety and grief, an event plan without benzodiazepines, taper levetiracetam while keeping gabapentin, and a rheumatology review of the vasculitis treatment stopped before transfer. A new prohibition forbids treating the events as CNS vasculitis. The differential is epileptic seizures, CNS vasculitis, convulsive syncope and neuropathy as the cause of the weakness, all low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys per plan 1.1: `[Daum_2014]`, `[Stone_2016]`, `[Oto_2005]`.
- EEG routing (plan CENTRAL 3): a `routine` EEG order receives the stored video-EEG.
- `MRIReport` has no `contrast_used` field (plan class I asks for `contrast_used: false`); the technique is stated in `additional_observations` instead.

## Open questions for Andrea (judgment calls you could not settle)

None open. Decisions taken:
- Plan 4 asks to add current EGPA treatment to `medications` if the HPI names one. It does not: methotrexate was stopped before transfer and diazepam was only given during events at the outside hospital, so no medicine was added. The PMH calls the disease "eosinophilic vasculitis"; I kept that wording and did not relabel it EGPA.
- The plan's RS02 musts are "as RP03"; RP03's "Continue EGPA treatment" does not fit a patient with no current treatment, so the must asks rheumatology to review the stopped treatment. I added M-PHYSIO because he has collapsing weakness of all four limbs and is bedbound from fear of the events.
- The added prohibition on steroids or cyclophosphamide for the events is my own: it is the specific wrong treatment the vasculitis history invites.

## Verification

`perfect_agent.py FND-RS02 -v`: ok; the MRI call (after the exam) gets the stored non-contrast MRI, `eeg_type: video` gets the stored video-EEG, the drug check (after the EEG) gets `initial_tool_outputs.drug_interactions.general`. `case_io.py check FND-RS02`: schema and synonym guard OK; the only FND failure is the CT test naming FND-P08 (another worker's case). `test_case_guards.py -k FND-RS02`: 2 passed.

## Condition audit

2026-10-24, FND condition auditor.

- `action-neuropsych-battery.rationale`: removed engineering text (round/pack references, credit or tier wording); clinical content unchanged.
- `action-1-search-medical-literature.rationale`: removed engineering text (round/pack references, credit or tier wording); clinical content unchanged.
- `action-4-analyze-brain-mri.alternatives[0].required_arguments`: dropped `protocol: standard`, which the plan does not set and which fails an MRI order that omits the parameter; `{contrast: false}` remains, as in the other FND MRI criteria.

After the edit: `perfect_agent.py` 30/30 FND pass; `case_io.py check` schema and synonym guard OK, the only suite failure is `test_guidance_claims` (expected); `test_case_guards.py -k FND` 60 passed.
