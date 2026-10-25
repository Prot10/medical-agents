# FND-RP03
Reviewer status: R1 none, R2 none (FND was never reviewed; no notes file) | Approved before this round: no

## Reviewer notes
No reviewer notes for this case.

| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | - |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | major | `ground_truth.action_criteria` | Template criteria (plan A): literature and drug check `recommended` with the shared labels, video-EEG, MRI and labs `optional`, labels equal to rationales, template citations. | FIXED: order exam (required), labs `["CBC","ESR","CRP"]` (recommended), brain MRI `{contrast: false, protocol: standard}` (recommended, CNS vasculitis question), video-EEG (required), drug check (required), new optional `action-neuropsych-battery`, literature (optional, last); case-specific labels, rationales, expected evidence, citations. |
| A | major | `ground_truth.sequence_constraints`, `.stop_rule` | No constraints; stop rule only the exam. | FIXED: soft exam before MRI, soft video-EEG before drug check (taper case, plan 3.3); stop rule exam, video-EEG, drug check; `max_additional_actions` 0. |
| C | major | `initial_tool_outputs.mri` | Post-gadolinium sequences and an MRA reported against a non-contrast criterion with no MRA criterion (plan I); impression a list of excluded diseases ("No evidence of CNS vasculitis"). | FIXED: non-contrast report (T1, T2, FLAIR, DWI/ADC, SWI) with a technique line; MRA parts removed (flow voids kept); punctate small vessel change and ethmoid thickening kept; impression "No acute intracranial abnormality..." without a disease list. |
| B | major | `initial_tool_outputs.eeg` | Impression not canonical; beta finding "unchanged from initial recording" (no initial recording) with an em dash; state text with interpretation ("EEG confirms cortical wakefulness") and scare-quoted 'recovery'. | FIXED: two event findings (four shaking events 15 to 40 s, three unresponsive events 75 to 120 s) with video semiology and the persisting alpha rhythm; canonical impression naming the seven events; beta called nonspecific. |
| D | major | `initial_tool_outputs.clinical_assessment` | Meta keys in `criteria_met`; tubular arm sensory loss counted as a sign; key-leak impression. | FIXED: canonical shape; 3 validated signs counted (bilateral Hoover, collapsing weakness, distractibility) plus examination-function inconsistency; arm sensory loss supportive; neuropathy signs reported separately; observed event row; event-based impression. |
| C | major | `patient.neurological_exam.motor` | Hoover sign described as "synergistic extension of the left heel ... then absent during direct left hip flexion testing" (heel extension tested with the wrong movement). | FIXED: "hip extension is weak on direct testing on each side but full during flexion of the opposite hip against resistance". Em dashes in motor and sensory removed; "glove distribution" for a whole-arm loss reworded. |
| D | major | `initial_tool_outputs.labs` | B12 row without a usable value; "Post_Event_Prolactin" panel holding a baseline value; interpretation with management text. | FIXED: B12 412 pg/mL (normal), `clinical_significance` null; panel renamed "Prolactin"; plain interpretation of the abnormal values; other values unchanged. |
| C | major | `followup_outputs[*]` (drug check) | Sertraline output for a drug he does not take, claiming levetiracetam "can be tapered over 1-2 weeks"; prednisolone with metformin, tamsulosin with diazepam and levetiracetam mood effects absent. | FIXED: deleted; `initial_tool_outputs.drug_interactions.general` lists the six medicines verbatim with prednisolone raising glucose on metformin, diazepam with tamsulosin (orthostasis, falls), diazepam with levetiracetam (sedation), mood effects of levetiracetam and prednisolone, gradual withdrawal; no dose or new drug. |
| D | major | `followup_outputs[*]` (literature) | Case-agnostic follow-up with misattributed sources (plan B). | FIXED: deleted; canonical `initial_tool_outputs.literature_search`. |
| C | major | `ground_truth.assessment.required_recommendations` | Template musts; no taper plan; vasculitis treatment not addressed. | FIXED: M-DX (functional seizures with functional limb weakness), M-COMM, M-PHYSIO, M-PSY (health anxiety, grief, caregiver strain), M-RESCUE, M-ASM (levetiracetam then diazepam, one at a time), continue the vasculitis treatment and prednisolone taper with rheumatology. |
| C | major | `ground_truth.assessment.prohibited_recommendations` | "per Stone 2018"; "start or continue" AEDs. | FIXED: P1, P2, P3, P5 with "or stop it abruptly", P6, P7, and "Treat the events as CNS vasculitis with high-dose corticosteroids or cyclophosphamide". |
| C | major | `ground_truth.differential` | Epileptic seizures `moderate` after seven recorded events; structural, encephalitis and malingering template rows; CNS vasculitis, syncope and neuropathy questions missing. | FIXED: epileptic seizures `low` (canonical), CNS vasculitis `low` (MRI, no focal deficit, no ictal change), convulsive syncope or arrhythmia `low` (telemetry, speech during shaking), diabetic neuropathy as the cause of the weakness `low`. |
| B | minor | `ground_truth.red_herrings` | Generic data points and Stone 2018. | FIXED: the vasculitis with the referring hypothesis, raised eosinophils, ESR and CRP, the white matter change, the paternal aunt's epilepsy, the remote anxiety and bereavement, each with the case's data. |
| E | major | `ground_truth.key_clinical_evidence` | Template items with the "Interim composition decision" leak, OPTIONAL item and Stone 2018. | FIXED: 5 case-specific items. |
| C | minor | `ground_truth.avoided_actions[*]` | `[Stone_2018]`; generic rationales. | FIXED: `[Espay_2018]`/`[Stone_2016]`, patient-specific rationales (telemetry already negative, neuropathy already known); all kept as waste. |
| B | minor | `fallback_tool_outputs` | specialized_test and advanced_imaging untyped with the leak sentence; echo "benign incidental finding" unnamed, no `echo_type`. | FIXED: nulled and removed from `fallback_tool_kinds`; echo `echo_type: TTE`, impression names mild aortic valve sclerosis without stenosis. |
| B | minor | `metadata.difficulty_description`, `.difficulty_rationale`, `.estimated_complexity` | Named an anti-GAD65 result the case does not contain; template rationale. | FIXED: rewritten from the case's data; `last_revised` 2026-10-24. |

## Changes, in one paragraph a physician can read before re-reviewing

The pathway is the examination (required), blood count with ESR and CRP and a non-contrast brain MRI (both recommended, for the referring team's CNS vasculitis question, MRI after the examination), the 4-day video-EEG (required) and the medication review (required, after the video-EEG), with optional neuropsychology and literature last. The examination report now describes the Hoover sign correctly on both sides, counts it with collapsing weakness and distractibility, notes the gait that normalizes when he is unobserved, keeps the diabetic neuropathy signs apart and the whole-arm sensory loss as supportive, and describes the witnessed two-phase event. The video-EEG names all seven habitual events, of both types, without ictal change. The MRI is a non-contrast report without the gadolinium sequences and MRA it used to contain; it shows only punctate small vessel change. The B12 now has a value and the prolactin panel is no longer called post-event. The drug check replaces a sertraline output (he takes none) with prednisolone raising glucose on metformin, diazepam with tamsulosin and levetiracetam, and the mood effects of levetiracetam and prednisolone. Musts: positive diagnosis, explanation, physiotherapy, psychological therapy for health anxiety and grief, an event plan without benzodiazepines, levetiracetam then diazepam withdrawn one at a time, and continued vasculitis treatment with rheumatology. A new prohibition forbids treating the events as CNS vasculitis. The differential is epileptic seizures, CNS vasculitis, convulsive syncope and neuropathy as the cause of the weakness, all low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys per plan 1.1: `[Daum_2014]`, `[Stone_2016]`, `[Oto_2005]`.
- EEG routing (plan CENTRAL 3): a `routine` EEG order receives the stored video-EEG.
- `MRIReport` has no `contrast_used` field (plan class I); the technique is stated in `additional_observations`.

## Open questions for Andrea (judgment calls you could not settle)

None open. Decisions taken:
- The plan's RP03 musts do not list M-PHYSIO; I added it because he has collapsing weakness of four limbs and a gait disorder with fear of falling (the plan's motor-phenotype rule).
- The plan says "Continue EGPA treatment"; the case calls the disease "eosinophilic vasculitis" and never names EGPA, so the must and the differential row keep the case's wording.
- The added prohibition on steroids or cyclophosphamide for the events is my own, matching RS02 (same source patient): it is the specific wrong treatment the vasculitis history invites.
- B12 412 pg/mL is a new value: the original row had none, and a normal value is what the interpretation already implied.

## Verification

`perfect_agent.py FND-RP03 -v`: ok; the exam gets the clinical assessment, the lab and MRI calls get the stored reports, `eeg_type: video` gets the stored video-EEG, the drug check (after the EEG) gets `initial_tool_outputs.drug_interactions.general`. `case_io.py check FND-RP03`: schema and synonym guard OK; no test failure names this case. `test_case_guards.py -k FND-RP03`: 2 passed. No em or en dashes left in the case.

## Condition audit

2026-10-24, FND condition auditor.

- `action-neuropsych-battery.rationale`: removed engineering text (round/pack references, credit or tier wording); clinical content unchanged.
- `action-1-search-medical-literature.rationale`: removed engineering text (round/pack references, credit or tier wording); clinical content unchanged.
- `action-4-analyze-brain-mri.alternatives[0].required_arguments`: dropped `protocol: standard`, which the plan does not set and which fails an MRI order that omits the parameter; `{contrast: false}` remains, as in the other FND MRI criteria.

After the edit: `perfect_agent.py` 30/30 FND pass; `case_io.py check` schema and synonym guard OK, the only suite failure is `test_guidance_claims` (expected); `test_case_guards.py -k FND` 60 passed.

## Close-out (24 Oct 2026)

Andrea's FND ruling of 24 Oct 2026 and the close-out decisions (`plans/FND-decisions.md`). What changed and why:

- `action-5-analyze-eeg` (video-EEG) required -> optional, removed from the stop rule; 1 soft constraint(s) naming it removed; rationale now says what the diagnosis rests on without the recording (ILAE 2013 levels).
- M-DX must, COMM must, red-herring interpretations and metadata no longer say the diagnosis rests on the video-EEG: they rest on the positive signs and the event semiology, with video-EEG confirmation where recorded (open question 8).
- M-ASM taper must now conditions the taper on a secure diagnosis, ideally documented on video-EEG.
- Diagnosis synonyms scoped by phenotype (`diagnosis_synonyms.yaml` F44 entries; a label or code naming another presentation must not score): removed "functional movement disorder"; added "psychogenic nonepileptic seizures", "dissociative seizures", "nonepileptic seizures", "functional limb weakness", "functional motor disorder".
- The medicine review stays required as a management act (ruling); listed for the physicians in `plans/FND-decisions.md`.
- Checks: `perfect_agent.py -v` and `case_io.py check` clean; `test_case_guards.py -k FND-` passes, now including the discriminator guard.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `video`, named in the report's own text.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Library contradictions (25 Oct 2026)

Orders that reached the benchmark library's normal report although the case contradicts it now get a case-specific report (library answers stay for everything else).

- `perform_clinical_assessment assessment_type=gait_and_balance_timed` -> `fallback_tool_outputs.clinical_assessment`: timed gait and balance: 17.2 s TUG, lurching gait with excessive side-to-side sway, without a fall. Why: the exam documents an abnormal gait; the library reports a normal timed gait (TUG 9.1 s).
- `perform_clinical_assessment assessment_type=performance_status` -> `followup_outputs[request_performance_status]`: Karnofsky 70, ECOG 2. Why: the history documents limited activity; the library reports Karnofsky 100, ECOG 0, working.
- `order_specialized_test test_type=neuropsych_battery` -> `followup_outputs[request_neuropsych_battery]`: cognition within normal limits; abnormal anxiety, borderline depressive symptoms, elevated health anxiety and mildly elevated dissociative experiences; validity passed. Why: the history documents anxiety, depression or trauma-related symptoms; the library reports no significant mood or anxiety symptoms.
- `order_specialized_test test_type=emg_ncs` -> `fallback_tool_outputs.specialized_test`: moderate length-dependent axonal sensorimotor polyneuropathy; proximal muscles normal. Why: known diabetic distal symmetric sensorimotor neuropathy with reduced ankle reflexes and stocking sensory loss; the library reports normal nerve conduction.
- `order_specialized_test test_type=skin_biopsy_iencf` -> `followup_outputs[request_skin_biopsy_iencf]`: distal IENFD 3.2/mm (reduced), proximal normal. Why: known diabetic peripheral neuropathy; the library reports normal nerve fibre density.

Checks: `perfect_agent.py` pass; `test_case_guards.py -k FND-RP03` pass; map verify (map_FND) problems 0; criterion-answer snapshot unchanged except `action-neuropsych-battery`, which the library answered before and the new report now answers.
