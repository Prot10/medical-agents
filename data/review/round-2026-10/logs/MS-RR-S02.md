# MS-RR-S02
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for MS-RR) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. All changes below are own findings and plan classes. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `followup_outputs[2]` (OCT) | Right pRNFL 72 / GCIPL 64 thinning 14 days into a first optic neuritis (plan I, F7; no prior visual episode); impression a bare "Abnormal values" list. | FIXED: acute form, both eyes labelled (R pRNFL 105, GCIPL 79; L 101, 82; inter-eye 4 and 3 um); impression "within normal limits ... no thinning". |
| B | minor | `patient.neurological_exam.cranial_nerves` | Fundus not described in an optic neuritis exam. | FIXED: "normal optic discs bilaterally, with no swelling or pallor" (retrobulbar, matches the 12 mm retrobulbar MRI segment and the normal OCT). |
| B | minor | `followup_outputs[0].output` (spine MRI) | Right-predominant pyramidal signs (right Babinski, right ankle dorsiflexion 4+/5, right circumduction) with a C3-C4 "dorsolateral" lesion of unstated side and a dorsal-column T6-T7 lesion; empty descriptions. | FIXED: C3-C4 lesion placed right dorsolateral; descriptions (length under one segment, cross-section, enhancement); numbered impression. |
| A/C | major | `followup_outputs` (`request_repeat_mri_3months`) | Future 3-month MRI served in the current work-up (class F). | FIXED: deleted. |
| C | major | `followup_outputs` (drug check) | Natalizumab check stated an anti-JCV index of 0.3 and negative hepatitis B/C and HIV, none of which the case contains (fabricated results in an any-query output); empty `interactions`; DMT alternatives listed by efficacy. | FIXED: rewritten for the drug the case actually needs now, methylprednisolone: ibuprofen with high-dose steroids (GI bleeding; avoid or PPI), vitamin D3 no interaction, infection exclusion, glucose and BP warnings; trigger `request_drug_interaction_check_steroids`. |
| C | major | `followup_outputs` (literature) | AAN 2018 and ECTRIMS/EAN 2018 summarised with claims they do not make ("early aggressive therapy preferred", "vitamin D supplementation recommended as adjunct"); DMT choice argued. | FIXED: canonical general 2024 McDonald text (class O), trigger `search_mcdonald_criteria`. |
| C | major | `ground_truth.action_criteria` | Template criteria (literature/drug required with unmatched arguments; CSF needing three assays; labs with 11 analytes and embedded AQP4/MOG; label = rationale; unverifiable free-text citations). | FIXED per plan A/P: brain MRI, spine MRI, labs (required), `action-aqp4-mog-cba` (recommended), CSF, VEP, OCT, drug check, literature (optional); case-specific rationales and evidence; bracketed keys only. |
| C | minor | `ground_truth.stop_rule` | Literature and drug check in the stop rule; max 0. | FIXED: brain MRI, spine MRI, labs; max 2. |
| C | major | `ground_truth.assessment` | Template musts (DIS/DIT restatements, AQP4/MOG test as a must, generic IV steroid, JCV, smoking cessation in a never smoker); no infection exclusion or bladder management despite urinary urgency; JCV and fingolimod prohibitions with no case reason. | FIXED: formulation must; urinalysis/culture before steroids, then IV 1 g x3-5 d or oral 500 mg x5 d, ibuprofen avoided or PPI, PLEX if refractory; DMT by activity with pregnancy/contraception; pre-DMT screening; post-void residual with antimuscarinic or ISC (> 100 mL). Prohibitions: non-specific lesions, teriflunomide, chronic steroids, live vaccines, cord MRI, and "do not attribute to lumbar radiculopathy"; JCV and fingolimod deleted. |
| C | major | `ground_truth.differential` | NMOSD and MOGAD "high", sarcoidosis "moderate" after negative CBA, normal ACE and short cord lesions. | FIXED: all low with the case's results; added B12 myelopathy, NPSLE (ANA row) and neurosyphilis (CSF VDRL row); CNS vasculitis and Susac removed (nothing in the case raises them), ADEM low. |
| C | major | `ground_truth.key_clinical_evidence` | Engineering lines, wrong facts (three regions establish DIS; black holes give DIT; OCB substitute for DIT), tumefactive line, ELISA line, DMT line, generic cord-imaging line. | FIXED: six observable bullets (optic neuritis, myelopathy with its lesions, DIS 5 of 5 with sites, prior attack, mimic exclusion, vitamin D). |
| E | minor | `initial_tool_outputs.labs` | AQP4 row "NMO-IgG (Aquaporin-4 antibody)" without method; panel "Autoimmune and MS-specific" mixing B12, TSH, ACE and vitamin D; HIV row with leaked significance; BMP only. | FIXED: panels CBC, CMP (albumin, ALT, AST, ALP, bilirubin added, normal), inflammatory markers, vitamins and endocrine, autoimmune (ANA, ACE), neuroimmunology (CBA rows), infectious serology (HIV, significance null). Red herring field path updated to `panels.Vitamins and endocrine[2]`. |
| B | minor | `initial_tool_outputs.labs.panels.CBC` (Hematocrit) | Hb 14.4 g/dL with Hct 38.8% gives MCHC 37.1 g/dL (above the physiological maximum). | FIXED: Hct 42.6% (MCHC 33.8). |
| C | minor | `initial_tool_outputs.csf` | Myelin basic protein (obsolete, F6); no kFLC; protein, glucose and WBC without reference ranges; recital interpretation; IgG index 0.82 and synthesis rate 12.4 identical to S01 (template numbers). | FIXED: MBP deleted; kFLC 24.7 (< 6.1) added; references added (protein 49.1 is mildly raised against 15-45); IgG index 0.91, synthesis 14.8; pattern interpretation. |
| B | minor | `followup_outputs[1]` (VEP) | Values identical to S01 (128 ms, 3.2/8.1 uV). | FIXED: right P100 124 ms, 4.1 uV; left 103 ms, 7.6 uV; inter-eye 21 ms; impression adjusted. |
| D | minor | `initial_tool_outputs.mri` | Impression a prose run-on; no statement that the cord was outside the study. | FIXED: numbered impression of brain and optic nerve findings; "Spinal cord not assessed on this study."; callososeptal lesions named as periventricular. |
| B | minor | `patient.clinical_history.allergies` | "Contrast dye (mild reaction)" while gadolinium MRI is required (plan R). | FIXED: "Iodinated CT contrast (mild urticaria)". |
| E | minor | `fallback_tool_outputs.drug_interactions.general.proposed` | "(agent not specified on this case's pathway)": benchmark wording in a served output. | FIXED: "Not specified". |
| A | minor | `fallback_tool_outputs.advanced_imaging.modality` | "FDG-PET" prose. | FIXED: `FDG_PET`. |
| C | minor | `ground_truth.avoided_actions`, `red_herrings`, `metadata.difficulty_rationale` | Generic rationales with em dashes; single herring; 2017 wording. | FIXED: case-tied rationales; radiculopathy herring added (`past_medical_history[0]`); metadata in 2024 terms, `last_revised` 2026-10-24. |
| A | minor | `ground_truth.differential[*].icd_code` | Neurosarcoidosis coded D86.85 (sarcoid myocarditis); ADEM coded G04.81 (other encephalitis); ICD-10-CM codes neurosarcoidosis D86.89 and ADEM G04.00. | FIXED: D86.89 and G04.00. |

## Changes, in one paragraph a physician can read before re-reviewing

A 31-year-old woman with two weeks of right optic neuritis (20/60, RAPD) and a concurrent myelitis (right-predominant spastic paraparesis, T10 level, urgency, Lhermitte), after a leg attack 8 months ago. The fundus is now documented as normal and the OCT shows no thinning at two weeks; the VEP keeps a prolonged right P100 (now 124 ms, no longer S01's numbers). The brain MRI impression lists brain and optic nerve findings only; the spine MRI places the C3-C4 lesion right dorsolateral (matching the right pyramidal signs) and describes both short lesions. The 3-month repeat MRI was deleted. The drug check now screens methylprednisolone against her ibuprofen instead of a natalizumab check that invented an anti-JCV index and viral serology; the literature output no longer misquotes the AAN and ECTRIMS guidelines. Work-up: brain MRI, spine MRI, mimic labs (required), AQP4/MOG CBA (recommended), CSF, VEP, OCT, drug check, literature (optional). CSF drops myelin basic protein and adds kFLC 24.7. Musts: 2024 McDonald formulation (5 of 5 regions), urinalysis before steroids then methylprednisolone with ibuprofen stopped or PPI cover, DMT by activity with pregnancy and contraception discussed, pre-DMT screening, post-void residual and bladder management. Differential all low with reasons (NMOSD, MOGAD, sarcoidosis, B12, NPSLE, neurosyphilis, ADEM).

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys `[McDonald_2024]`, `[Wattjes_2021]`, `[NICE_NG220]` (plan 5.1); synonyms G35.B/G35.C and "demyelinating disease" (plan 5.2).
- `perfect_agent.py` prints `<- ?` for the brain MRI and labs sources (its `_source` compares an `exclude_none` dump with an output that keeps null fields); a direct environment probe confirms both come from the case's initial outputs.

## Open questions for Andrea (judgment calls you could not settle)

None. The drug check now addresses the acute steroid course rather than a DMT; the DMT choice stays with the clinician (DMT must) and no DMT-specific drug check is scored.

## Verification

`perfect_agent.py MS-RR-S02 -v`: ok (spine <- followup[0]; brain MRI and labs/AQP4-MOG <- initial outputs, probe-confirmed). Probe: CSF (OCB or kFLC), VEP, OCT, drug check, literature served from the case; CT and FDG-PET from case fallbacks. `case_io.py check MS-RR-S02`: schema and synonym guard OK, no failure names S02. `test_case_guards.py -k MS-RR-S02`: pass.
