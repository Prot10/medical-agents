# MS-RR-M04
Reviewer status: R1 none, R2 none (no MS-RR notes file in this round) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case. All changes below are own findings and plan classes. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | minor | `patient.clinical_history.past_medical_history[2]` | "No prior neurological diagnoses or episodes" contradicts the HPI's right arm and trunk sensory episode 8 months ago. | FIXED: "No prior neurological diagnoses". |
| C | major | `ground_truth` framing (KCE, musts, prohibitions, differential, red herring 0, `metadata.difficulty_rationale`, `.condition_name`) | Built as "CIS meeting McDonald 2017 via OCB-for-DIT": called this a first attack despite the HPI's prior attack, and said "MRI alone does NOT establish DIT, making the CSF OCB load-bearing", which is wrong under the 2024 criteria with five regions (plan M04, F3). | FIXED: rewritten as two attacks with 5 of 5 regions (PV, JC, IT, cord C5-C6, optic nerve), no DIT needed, CSF supportive; the CIS trap kept as a red herring and a low differential entry. |
| D | minor | `initial_tool_outputs.mri.impression`, `.additional_observations[1]` | Impression applied criteria ("at least three of four characteristic MS regions", 2017 count); observation phrased as a DIT verdict. | FIXED: numbered findings-only impression; observation "enhancement is confined to the left optic nerve". |
| B | minor | `initial_tool_outputs.labs` | AQP4/MOG row names did not match the canonical CBA labels; vitamin D 18 ng/mL copied across cases (plan E); summary carried interpretive text; Hct 40.1 with RBC 4.41 and MCV 88.4 inconsistent. | FIXED: "AQP4-IgG (cell-based assay)", "MOG-IgG (live cell-based assay)"; vitamin D 21 ng/mL; plain summary and interpretation; Hct 39.0. |
| C | minor | `initial_tool_outputs.csf` | MBP (obsolete); no kFLC (plan J). | FIXED: MBP deleted, kFLC 38.6 (reference < 6.1), pattern interpretation; values unchanged. |
| C | major | `followup_outputs` literature | 2017 criteria and MAGNIMS 2016 "2 of 4 regions" presented as current; summary restated the case's OCB-for-DIT key (plan O). | FIXED: McDonald 2024 result (general), Reich 2018 kept for the ON-as-presentation fact only; summary general. |
| C | minor | `followup_outputs` drug check `.warnings`, `.interactions` | Natalizumab risk threshold stated as "index > 0.9 and prior immunosuppressant use"; vitamin D3 and the sulfonamide allergy not listed (plan F11, O). | FIXED: index above 1.5 high risk, duration > 2 years, prior immunosuppression; two lines added. |
| B | minor | `followup_outputs` OCT `.impression`, VEP, spine | Missing final periods; OCT impression silent on the slight left swelling; empty spine lesion description. | FIXED. Values unchanged; OCT normal in the acute phase is correct (F7). |
| A | major | `ground_truth.action_criteria` | AQP4/MOG embedded in the labs criterion (11 analytes); literature and drug check required with non-schema keys; CSF requiring three assays; free-text citations (plan A). | FIXED: labs `{CBC, vitamin_B12, TSH, HIV}`; `action-aqp4-mog-cba` required (hand-motion acuity is a red flag); CSF, VEP, OCT, drug check, literature optional; literature last. |
| A | minor | `ground_truth.stop_rule`, `.sequence_constraints` | Literature and drug check in the stop rule; max 0. | FIXED: brain MRI, spine MRI, labs, AQP4/MOG; max 2; canonical soft MRI-before-CSF. |
| C | major | `ground_truth.assessment.required_recommendations` | Must 1 applied 2017 OCB substitution with "spinal cord on follow-up MRI"; must 2 a disguised test; HBV must duplicated in DMT must. | FIXED: formulation; MS-not-CIS explanation; IVMP (or oral) for severe ON with PLEX if no improvement; DMT with contraception discussion (COC); pre-DMT screening; Uhthoff counselling (reported). |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | NMOSD-diagnosis prohibition restated the differential; fingolimod prohibition without cardiac reason (plan M04, K). | FIXED: deleted; CIS-deferral prohibition reworded to the 2024 basis; ELISA prohibition kept; added low-dose oral prednisolone alone (ONTT), T7, T11. |
| C | major | `ground_truth.differential` | CIS "very_high", NMOSD/MOGAD "high" with negative CBA, ADEM "moderate"; neurosarcoidosis cited a normal ACE that the labs do not contain; codes D86.85, G04.81. | FIXED: all low with the case's results; sarcoid entry cites calcium and imaging only; D86.89, G04.00. |
| D | major | `ground_truth.key_clinical_evidence` | Benchmark wording ("red herring to avoid"), "July 2026" engineering lines, 2017 framing (plan D). | FIXED: six observable lines. |
| B | minor | `ground_truth.avoided_actions`, `fallback_tool_outputs.echo` | Generic rationales; echo without `echo_type`. | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

A 26-year-old woman with five days of severe painful left optic neuritis (hand motions, 3+ RAPD, mild disc swelling) and a right arm and trunk sensory episode 8 months ago that was attributed to stress. The case was built as "CIS meeting McDonald 2017 by OCB substitution". It now follows the 2024 criteria: lesions in five of five regions (four periventricular, left parietal juxtacortical, dorsal pons, right dorsolateral C5-C6 cord, left optic nerve on MRI and VEP) establish MS without a separate DIT test, and the CSF (five restricted bands, kFLC 38.6 added, MBP removed) is supportive. The brain MRI impression lists findings only. The literature output describes the 2024 revision. AQP4-IgG and MOG-IgG by cell-based assay are a separate required criterion (red flag: hand-motion acuity) and are negative. Pathway: brain MRI, spine MRI, labs and AQP4/MOG required; CSF, VEP, OCT, drug check and literature optional. Musts: formulation, telling her she has MS (not CIS), IV methylprednisolone with PLEX if no recovery, DMT with a contraception discussion, pre-DMT screening, Uhthoff counselling. Prohibitions: no CIS deferral, no ELISA, no low-dose oral prednisolone alone. All mimics low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys `[McDonald_2024]`, `[Wattjes_2021]`, `[NICE_NG220]` (plan 5.1); synonym codes G35.B/G35.C and "demyelinating disease" (plan 5.2).

## Open questions for Andrea (judgment calls you could not settle)

- None.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the diff and the whole final case. No reviewer notes exist for MS-RR; the table correctly says so.
Checked: reframing from "CIS by 2017 OCB substitution" to two attacks with 5 of 5 regions is correct under the 2024 criteria and matches the reports (four PV, left parietal JC, dorsal pons, right dorsolateral C5-C6 fitting the earlier right arm and trunk episode, left optic nerve on MRI and VEP); normal OCT at day 5 is correct (F7); AQP4/MOG required and in the stop rule (hand-motion acuity); musts and prohibitions consistent (COC contraception discussion, ONTT low-dose prednisolone prohibition, teriflunomide/cladribine contraception); drug check facts match F11; literature general and correctly cited; differential all low with reasons.
Found and fixed:
- The CNS vasculitis entry of the differential cites "ESR/CRP normal", but the stored labs contained no ESR or CRP (the pre-round criterion had required them while the report never carried them). Added an "Inflammatory markers" panel (ESR 10 mm/hr, CRP 0.2 mg/dL, both normal) to `initial_tool_outputs.labs.panels` and named ESR and CRP in the labs criterion's expected evidence.
Checks re-run after the changes: `perfect_agent.py -v` pass, `case_io.py check` clean for the case, `test_case_guards.py -k` (leak, follow-up, banned strings) pass.
