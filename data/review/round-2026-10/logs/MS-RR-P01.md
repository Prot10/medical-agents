# MS-RR-P01
Reviewer status: R1 none, R2 none (no MS-RR notes file in this round) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case. All changes below are own findings and plan classes. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | blocker | `followup_outputs` `request_repeat_mri_3months`, `initial_tool_outputs.mri` | The label rested only on a brain MRI from three months in the future (new enhancing periventricular and juxtacortical lesions); the index MRI had five non-specific subcortical foci, no infratentorial lesion and no enhancement, so at the encounter the data could not support MS (plan F, P01). | FIXED: future scan deleted. The index MS-protocol MRI now also reports an 8 mm ovoid right periventricular lesion perpendicular to the ventricle with incomplete ring enhancement and a 6 mm left middle cerebellar peduncle lesion (explains the vertigo episodes); the five original foci are kept; impression neutral and findings-based ("pattern includes lesions typical of inflammatory demyelination; the small subcortical foci are non-specific..."); "No infratentorial lesions" and "No spinal cord lesion visible" observations replaced. The HPI's outside "nonspecific" MRI stays as history (different, non-protocol study). |
| B | minor | `followup_outputs[0].output` (spine MRI) | C3-C4 lesion with no side and no enhancement although the right hand clumsiness began 4 days ago. | FIXED: right dorsolateral, faint enhancement, under half the cross-section; description filled; impression updated. |
| B | major | `followup_outputs` VEP | Both P100 latencies normal yet the study called ABNORMAL for a "markedly prolonged" 10 ms interocular difference (plan P01). | FIXED: left P100 119 ms (prolonged), right 102 ms, difference 17 ms; impression consistent; the optic nerve region now counts (subclinical). |
| B | minor | `initial_tool_outputs.labs.panels.CBC` | Hct 35.6 with RBC 4.01 gives MCV 88.8, not the stored 79.8. | FIXED: RBC 4.46 x10^6/uL (Hct and MCV unchanged). |
| B | minor | `initial_tool_outputs.labs` | ANA 1:40 flagged normal against "Negative (<1:40)"; B12, TSH and folate under "Autoimmune_Screen"; HIV row with leaked significance (plan E); no liver tests. | FIXED: ANA `is_abnormal` true and listed; panels regrouped; HIV significance null; LFTs added; interpretation recites the abnormal values. No AQP4/MOG result stored (plan 3.2: none for P01). |
| C | minor | `initial_tool_outputs.csf` | MBP (obsolete); no kFLC (plan J). | FIXED: MBP deleted; kFLC 3.2 (reference < 6.1), below the cutoff (the OCB-negative puzzle is kept); pattern interpretation. |
| C | major | `followup_outputs` drug check | "Topiramate: Both may cause lymphopenia" is false (plan F11); other medicines and the codeine intolerance not listed. | FIXED: topiramate, escitalopram, sumatriptan, ibuprofen each no significant interaction; codeine line; lymphocyte rule worded as in the label. |
| C | major | `followup_outputs` literature | 2017 criteria and MAGNIMS 2016 "2 of 4 regions" presented as current (plan O). | FIXED: McDonald 2024 (general text) and Solomon 2016 (Neurology) on migraine as the commonest MS misdiagnosis. |
| A | major | `ground_truth.action_criteria`, `.stop_rule`, `.sequence_constraints` | Template criteria (plan A, P, 3.4). | FIXED: brain MRI, spine MRI, labs required; CSF recommended; VEP, drug check, literature optional, literature last; no AQP4/MOG criterion; stop rule = the three required, max 3; soft MRI-before-CSF. |
| C | major | `ground_truth.assessment` | Template musts (T0-T2, IV steroids for a relapse that is resolving and does not affect function, smoking cessation in a never smoker); JCV and fingolimod prohibitions without a case reason; T13 although there are no myelopathic signs. | FIXED: formulation; no steroids for the mild improving relapse (steroids only for one affecting function); DMT with pregnancy/contraception discussion noting topiramate teratogenicity; pre-DMT screening. Prohibitions: T7, negative OCB do not exclude MS, do not attribute all lesions to migraine, T10, T11, T12. |
| C | major | `ground_truth.differential` | NMOSD/MOGAD high, sarcoid moderate; the case's own mimics (migraine lesions, vestibular migraine, lupus with a family history and ANA) absent. | FIXED: migraine-related WML, vestibular migraine, small vessel disease, CNS lupus/APS, NMOSD, MOGAD, B12, Susac, all low with the case's reasons. |
| D | major | `ground_truth.key_clinical_evidence` | Template lines (plan D). | FIXED: six observable lines (attacks, DIS 4 of 5, enhancement, cord lesion as supporting evidence and negative CSF, migraine foci, distractors). |
| B | minor | `ground_truth.red_herrings` | Empty although the case is built on distractors. | FIXED: outside nonspecific MRI and vestibular-migraine label; negative CSF; ANA with family lupus. |
| E | minor | `metadata.difficulty_rationale`, `.mcdonald_criteria_met_at`, `.requires_longitudinal_followup` | Described the diagnosis as needing the follow-up MRI. | FIXED: met at the initial work-up; longitudinal follow-up false. |
| B | minor | `ground_truth.avoided_actions`, `fallback_tool_outputs.echo` | Generic rationales; echo without `echo_type`. | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

A 25-year-old woman with migraine, 18 months of vertigo episodes labelled vestibular migraine, months of foot tingling and 36 hours of right hand clumsiness 4 days ago, an outside "nonspecific" MRI and a normal exam. Previously only a scan from three months in the future made the diagnosis; that scan is gone, and the index MS-protocol MRI now shows, beside the five small migraine-type foci, an enhancing ovoid right periventricular lesion and a left middle cerebellar peduncle lesion. The cord MRI shows a short right dorsolateral C3-C4 lesion with faint enhancement, and the VEP a subclinical left P100 delay (119 ms; previously both latencies were normal). DIS is 4 of 5 regions; the cord lesion is the supporting evidence that migraine-type foci call for; CSF stays negative (no restricted bands, kFLC 3.2 added, MBP removed) as the puzzle's trap. The false topiramate-lymphopenia interaction was removed, and the literature output now describes the 2024 criteria and migraine misdiagnosis. Pathway: brain MRI, spine MRI, labs required; CSF recommended; VEP, drug check, literature optional. Musts: formulation; no steroids for the mild improving relapse; DMT with pregnancy counselling (topiramate is teratogenic); pre-DMT screening. Prohibitions include not excluding MS on negative OCB and not attributing all lesions to migraine.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys `[McDonald_2024]`, `[Wattjes_2021]`, `[NICE_NG220]` (plan 5.1); synonym codes G35.B/G35.C and "demyelinating disease" (plan 5.2).

## Open questions for Andrea (judgment calls you could not settle)

- None needing Andrea. Decision recorded: plan F4 lists migraine among the conditions for which the 2024 criteria recommend additional evidence. I could verify only the age over 50 and vascular risk factor wording, so the case states it as clinical prudence ("migraine-type foci call for supporting evidence") and the literature output keeps to the verified wording. The lead may want to recheck the Montalban 2025 text and align P02/P03.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the diff and the whole final case. No reviewer notes exist for MS-RR; the table correctly says so.
Checked: the future MRI is gone and the index MS-protocol MRI now carries the typical lesions (enhancing ovoid right periventricular, left MCP for the vertigo) beside the original foci; impression neutral; right dorsolateral C3-C4 lesion fits the right hand clumsiness; VEP now has a prolonged absolute latency; DIS 4 of 5 and DIT by enhancement match the reports; OCB negative and kFLC below cutoff kept as the trap with a prohibition against excluding MS on negative CSF; no AQP4/MOG criterion or stored result (plan 3.2); false topiramate-lymphopenia line gone; no-steroids must correct for a mild resolving relapse (NICE NG220); the worker's handling of the unverified migraine wording in F4 is prudent.
Found and fixed:
- `initial_tool_outputs.mri.impression` item 3 counted "five small foci" and then added the left periventricular focus as a sixth, while the findings list five: reworded to "Five small foci: four subcortical/deep ... and a 3 mm left periventricular focus"; the brain MRI criterion's expected evidence follows.
- `patient.clinical_history.social_history.occupation` "marketing analyst" contradicted the HPI (graduate programme, typing her dissertation, graduate school stress, lives near campus): "Graduate student writing her dissertation" (pre-existing inconsistency the worker missed; P02 had the same class and was fixed).
Checks re-run after the changes: `perfect_agent.py -v` pass, `case_io.py check` clean for the case, `test_case_guards.py -k` (leak, follow-up, banned strings) pass.

## Condition audit

Condition auditor, 24 Oct 2026 (uniformity scripts over all 30 MS-RR cases; edits through `case_io`; perfect agent, `case_io check` and the case guards clean afterwards).

- `action-4-check-drug-interactions.expected_evidence` was empty; written from the stored drug output in policy voice: "Dimethyl fumarate with topiramate, escitalopram, sumatriptan and ibuprofen: no relevant interaction; lymphocyte monitoring for PML risk".
- `assessment.prohibited_recommendations[4]` chronic-steroid prohibition set to the condition's canonical text (was "Do not use chronic oral corticosteroids as a maintenance treatment for MS [em dash] they are ineffective long-term and carry significant harm").
- `assessment.required_recommendations[0]` formulation must made case-specific by appending "(here periventricular, infratentorial and spinal cord, completed by DIT from the enhancing and non-enhancing lesions, with the left optic nerve a fourth region by VEP)", from the KCE DIS line and the stored outputs, as in the other 18 cases.
- `assessment.required_recommendations[3]` pre-DMT screening: HIV removed from the tests to order and noted as already non-reactive, since the required mimic panel reports it (HIV-1/2 Ag/Ab combination assay: Non-reactive), as the RM, RP and RS cases do.

## Close-out (24 Oct 2026)

Condition close-out (`plans/MS-RR-decisions.md`). What changed and why:

- Diagnosis synonyms (`diagnosis_synonyms.yaml` G35 entry, re-applied with `apply_diagnosis_synonyms.py --prune --conditions multiple_sclerosis`): removed the label "demyelinating disease" (G37.9 is an Excludes1 of G35.A, and its tokens occur in an NMOSD, MOGAD or ADEM answer, which would have scored as correct) and the codes G35.B and G35.C (primary and secondary progressive MS in FY2026 ICD-10-CM, a different course from this relapsing-remitting case). Accepted now: the label, multiple sclerosis, MS, relapsing(-)remitting multiple sclerosis, RRMS; codes G35.A, G35, G35.D.
- `followup_outputs`: added the negative AQP4-IgG / MOG-IgG cell-based-assay follow-up (`interpret_labs`, trigger `request_aqp4_mog_cell_based_assay`, panel `Neuroimmunology`, after the spine MRI), as in the other 25 cases. The case has no AQP4/MOG criterion (no red flag, no optic neuritis or myelitis), so scoring is unchanged; before, an agent that ordered the assay received the first-line labs again with no antibody result (summary CENTRAL 5, open question 3). MockServer probe: all three alternatives, alone or with the mimic panel and in either order, receive the rows; the mimic panel alone does not.
- Checks: `perfect_agent.py` pass, `case_io.py check` clean for the case, `test_case_guards.py -k MS-RR-` passes with MS-RR now in `DISCRIMINATOR_CONDITIONS`.
