# MS-RR-RS04
Reviewer status: R1 not reviewed, R2 not reviewed (no MS-RR notes file in this round) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `initial_tool_outputs.mri.findings[4]`, `.additional_observations[2]`, `.impression`, `.volumetrics` | Brain MRI reported the C5-C6 cord lesion, "No longitudinally extensive transverse myelitis" and the cord in its impression (plan H). | FIXED: removed; "Spinal cord not assessed on this study."; count "9 supratentorial, 1 infratentorial"; numbered brain-only impression. |
| B | minor | `initial_tool_outputs.mri.findings[3].location`, `.additional_observations` | Lesion placed in the dorsal pons at the floor of the fourth ventricle "in the region of the abducens nucleus and fascicle": a nuclear lesion gives a horizontal gaze palsy, while the exam shows an isolated left abduction deficit (fascicular). | FIXED: "Left paramedian pontine tegmentum"; observation "lies along the intra-axial course of the left abducens nerve fascicle". |
| B | major | `patient.neurological_exam.sensory` | Light touch and pinprick loss in the right hand and pinprick loss in the right foot with "temperature intact": a left lateral column C5-C6 lesion explains contralateral (right) pain and temperature loss below the level, not light-touch loss, and pinprick and temperature travel together. | FIXED: "Decreased pinprick and temperature sensation over the ulnar side of the right hand and forearm and over the lateral right foot including the fifth toe. Light touch, vibration and proprioception intact." |
| C | major | `followup_outputs[request_repeat_mri_3months]` | Future 3-month MRI (plan F). | FIXED: deleted. |
| C | major | `followup_outputs[search_mcdonald_criteria_2017]`, `[search_cn6_palsy_demyelinating]` | 2017 criteria as current; the sixth-nerve output cites two references that could not be verified ("Nervig T, Barkhof F, Miller DH" J Neurol 2017; "Chen L, Gordon LK" J Neuroophthalmol 2015) and gives patient-directed management ("IV corticosteroids typically leads to resolution"). | FIXED: one general follow-up (`search_ms_diagnostic_criteria`, last) with the canonical 2024 text, Montalban 2025 and Wattjes 2021. |
| A | major | `ground_truth.action_criteria[action-3]`, `[action-4]`, `[action-5]`, `[action-6]` | Literature and drug check required with a typed query and non-schema keys; CSF required three assays; labs required 9 analytes. | FIXED: literature and drug optional `{}`; CSF optional (OCB or kFLC; 3 regions plus DIT on MRI); labs `{panels: [CBC, vitamin_B12, TSH, HIV]}`. No AQP4/MOG criterion and no stored result (plan 3.2: no optic neuritis, myelitis or red flag). |
| A | minor | `ground_truth.action_criteria[*]`, `.stop_rule`, `.sequence_constraints` | Label equals rationale; free-text citations; stop rule 0 with literature and drug check; pre-LP constraint cited McDonald 2017. | FIXED: canonical labels, case-specific rationales; order brain MRI, spine, labs, CSF, drug, literature; stop rule brain MRI, spine, labs, allowance 2; canonical soft constraint. |
| B | minor | `followup_outputs[0].output` (spine) | Empty lesion description. | FIXED: description; numbered impression. |
| C | major | `initial_tool_outputs.csf` | Myelin basic protein (F6); no kFLC; WBC 12, 5 bands, IgG index 0.78, synthesis 10.8, MBP 5.2 identical to RS01-RS03; "1 cell/microL (likely traumatic)"; Lyme CSF PCR and a viral PCR panel in an afebrile patient (not indicated; serum Lyme serology is already negative). | FIXED: WBC 8, protein 39, 6 bands, IgG index 0.81, synthesis 9.7, kFLC 22.3 (reference < 6.1); MBP and the PCRs removed; canonical interpretation that also states the normal opening pressure. |
| B | minor | vitamin D row, summary, interpretation, `red_herrings[0]` | 18 ng/mL copied across cases. | FIXED: 22 ng/mL. |
| C | minor | `followup_outputs[check_drug_interactions].output` | Dimethyl fumarate start without the 120 mg titration; acetaminophen and the sulfonamide allergy not checked; teriflunomide note about "the patient's partner" (he lives alone); lymphopenia rule worded as a hard withhold. | FIXED: titration; each medicine and the allergy listed; teriflunomide line per F11 (accelerated elimination, also for men wishing to father a child); SmPC-style monitoring wording. |
| C | major | `ground_truth.assessment.required_recommendations` | Template musts, AQP4 test as a must (not indicated here), IV-only steroid. | FIXED: formulation must (three regions, DIT from the enhancing pontine lesion, temporal subcortical lesion not a region); oral or IV steroid with BP and glucose monitoring plus occlusion or prism for diplopia; DMT by activity (no pregnancy clause: man); pre-DMT screening; vascular comorbidity; vitamin D. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | T10 (women) in a man; T8, T9 without trigger. | FIXED: deleted; kept T7, T11, T12, T13; added "Do not attribute the right hand and foot sensory symptoms to carpal tunnel syndrome or an ulnar neuropathy". |
| C | major | `ground_truth.differential` | NMOSD/MOGAD high, neurosarcoidosis moderate; IIH missing although the case pairs obesity with a sixth nerve palsy; the peripheral explanation the case itself offers (carpal tunnel) missing. | FIXED: all low with discriminating data; added IIH (G93.2, normal fundi and opening pressure), microvascular sixth nerve palsy (H49.20), Lyme neuroborreliosis (A69.22, serology negative), carpal tunnel or ulnar neuropathy (G56.00); NMOSD/MOGAD state that the antibodies were not tested and what argues against them. Susac and CNS vasculitis removed (nothing in the case raises them). |
| E | major | `ground_truth.key_clinical_evidence` | Engineering lines, F2/F5 wrong facts, template lines. | FIXED: six case-observable lines (palsy and lesion, contralateral sensory loss and prior episode, DIS 3 of 5, DIT and CSF, IIH excluded, distractor labs). |
| D | minor | `ground_truth.red_herrings` | The carpal tunnel attribution, the case's main distractor, was not recorded. | FIXED: second red herring at `patient.clinical_history.past_medical_history[2]`. |
| E | minor | `fallback_tool_outputs.advanced_imaging.modality`, `.echo` | "FDG-PET" prose instead of the vocabulary term; echo without `echo_type`. | FIXED: `FDG_PET`; `TTE`. |
| C | minor | `ground_truth.avoided_actions[*]` | Generic rationales and citations. | FIXED: case-tied; `[Wattjes_2021]` for CT and PET. |
| E | minor | `metadata.difficulty_*` | "McDonald 2017". | FIXED: 2024 wording with the IIH and carpal tunnel confounders. |

## Changes, in one paragraph a physician can read before re-reviewing

A 29-year-old obese hypertensive man with a one-day left sixth nerve palsy and right-sided sensory symptoms after a 2-week right hand episode 3 months ago that was called carpal tunnel syndrome. The brain MRI reports the brain only: an enhancing left paramedian pontine lesion along the abducens fascicle and non-enhancing periventricular lesions; the left lateral column C5-C6 lesion is in the spine report alone. The sensory exam now matches that lesion (right ulnar-side hand and lateral foot pain and temperature loss, light touch intact). The 3-month repeat MRI and the unverifiable sixth-nerve literature are gone. CSF: 6 bands, kFLC 22.3, opening pressure 14, no MBP or PCRs. Pathway: brain MRI, spine MRI, labs required; CSF, drug check (DMF titration corrected) and literature optional; no AQP4/MOG test (no red flag). Musts: RRMS by three regions plus MRI DIT; steroids with BP and glucose monitoring and diplopia occlusion; DMT; pre-DMT screening; vascular comorbidity; vitamin D 22. The differential adds IIH, microvascular palsy, Lyme and carpal tunnel, all low with their excluding data.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys `[McDonald_2024]`, `[Wattjes_2021]`, `[NICE_NG220]` (plan CENTRAL 1).
- Diagnosis synonyms G35.B/G35.C and "demyelinating disease" (plan CENTRAL 2); not hand-edited.

## Open questions for Andrea (judgment calls you could not settle)

None. The plan's "DIT by the enhancing pontine lesion" is applied; CSF stays optional because MRI already completes DIS with DIT.

## Verification

`perfect_agent.py MS-RR-RS04 -v`: pass; brain MRI <- initial MRI, spine <- `followup[0]`, labs <- initial labs. Brain MRI output has no C5 or cord lesion text. `case_io.py check`: schema and synonym guard OK, no failure naming MS-RR-RS04. `test_case_guards.py -k MS-RR-RS04`: 2 passed.
