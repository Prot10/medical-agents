# MIG-AURA-P06
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for MIG-AURA) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. July 2026 tool guidance applied through the plan (structured ICHD-3 history required; MRI for red flags; no CSF, ECG or routine echo). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | blocker | `patient.history_present_illness`, `patient.hpi` | The HPI quoted the outside MRI report ("highly suggestive of CADASIL... anterior temporal poles... external capsule... genetic testing strongly recommended") while brain MRI is a criterion (timeline leak, plan P06). | FIXED: replaced by "He had a brain MRI at a peripheral hospital 18 months ago... he does not know the result". The MRI output compares with that study. |
| B | minor | `patient.history_present_illness`, `patient.neurological_exam.mental_status`, `patient.physical_exam.general` | "works full-time as a retired solicitor who now does consultancy work" contradicts itself and the social history. | FIXED: retired solicitor working part-time as a legal consultant, in all three fields. |
| C | minor | `patient.neurological_exam.mental_status`, `patient.physical_exam.neurological` | MoCA losses called "age-appropriate subcortical reduction" (interpretation in the exam; an orientation error is not age-appropriate). | FIXED: values kept, interpretation removed ("1 point lost on orientation to date, 1 point on delayed recall"). |
| A | major | `initial_tool_outputs.clinical_assessment` | Template (class A): HPI sentences copied, the HPI opening sentence used as the "headache relation", generic red-flag line, placeholder modality score; criterion D set true although onset at 55 with a CADASIL family is exactly what D is about. | FIXED: rewritten with his data (3 attacks from 55, language aura developing over minutes by his account, 15-25 min, headache within about 15 min, family history, vascular risk, medicines, examination, red flags named). 4 of 6 kept; criterion D false with ICHD-3 6.8.1 (headache attributed to CADASIL) named. |
| D | major | `initial_tool_outputs.mri.impression` | "classical CADASIL imaging pattern... NOTCH3 gene sequencing required" (diagnostic conclusion plus a management-style instruction); no technique, comparison or microbleed statement. | FIXED: numbered impression, distribution "suggestive of CADASIL" (imaging-level), lacune, no acute infarct or microbleeds, unchanged from the outside study; technique and comparison added; structured findings unchanged. |
| D | major | `followup_outputs` (NOTCH3) | Report said "CADASIL CONFIRMED", children's 50% risk and "genetic counselling indicated" (management and family counselling in a lab report); `test_type` "genetic_panel". | FIXED: indication, technique (exons 2-24, familial variant confirmed), result c.544C>T p.(Arg182Cys) pathogenic, impression "This genotype confirms a diagnosis of CADASIL" (Kind 2); `test_type` `genetic_panel:CADASIL`. |
| A | major | `followup_outputs` (neuropsychology), `action-6` | Output `test_type` "neuropsychological_assessment" vs criterion `neuropsych_battery` (plan P06); one text blob. | FIXED: `neuropsych_battery`, findings per domain, same percentiles (7th, 10th, 15th), impression subcortical-pattern MCI without dementia; repeat in 12 months as a diagnostic recommendation. |
| C | major | `followup_outputs` (genetic counselling) | Consult disguised as a test (class O), with a DVLA notification claim that does not apply. | FIXED: follow-up deleted; genetic counselling for the children is now a must. |
| C | major | `followup_outputs` (two literature searches) | Invented titles (Chabriat 2009 "Migraine in CADASIL", Opherk 2004, Bousser 2012, Dichgans 2002, Singhal 2004, "ESO Guideline 2010"), aspirin recommendations without evidence, patient-shaped summaries. | FIXED: one literature follow-up kept, last, with real sources (Chabriat et al. Lancet Neurol 2009; Mancuso et al. EAN, Eur J Neurol 2020) and general statements; the anticoagulation search deleted. |
| C | major | `followup_outputs` (drug check), `action-2` | Criterion used `{"context": ...}` (unreachable, class C); output a follow-up with "formulary_status: contraindicated" and no check of his own medicines. | FIXED: output moved to `initial_tool_outputs.drug_interactions.sumatriptan` (served for any drug): no interaction with amlodipine, atorvastatin, paracetamol; triptans and ergots avoided in CADASIL (EAN 2020); NSAID warning with hypertension; alternatives. Criterion recommended (plan), alternatives sumatriptan, rizatriptan, zolmitriptan, triptan, ergotamine. |
| C | major | `ground_truth.action_criteria` (`action-1`) | Literature required with an exact query, in the stop rule (ruling 5). | FIXED: optional, `{}`, last, out of the stop rule. |
| C | minor | `ground_truth.action_criteria` (`action-4`, `action-5`, `action-6`, `action-3`) | MRI pinned `contrast: false, protocol: standard`; labels identical to rationales; `[AAN_2000]` cited for NOTCH3 and neuropsychology. | FIXED: MRI `{}`; labels, rationales and expected evidence rewritten from the case; citations per class N. |
| C | major | `ground_truth.assessment.required_recommendations` | Musts were tests ("Confirm CADASIL by NOTCH3 testing", "Establish baseline neuropsychological function", class J), vague risk-factor must, duplicated triptan avoidance. | FIXED: five musts: explain the diagnosis; aspirin or NSAID with antiemetic, no preventive at one attack a year; BP above target (136/82 on amlodipine 5 mg) to be increased towards below 130/80, statin, non-smoking; clinical genetics for the three adult children with the option not to test; repeat neuropsychology in 12 months. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Generic "do not prescribe ergotamines" and "do not anticoagulate without indication". | FIXED: triptans and ergots prohibited with the CADASIL reason (EAN 2020); anticoagulation without a compelling independent indication prohibited with the ICH reason. |
| C | major | `ground_truth.differential` | "Migraine with aphasic aura (sporadic)" high while the label is CADASIL; TIA moderate after the work-up (class F); familial Alzheimer raised by a red herring but absent. | FIXED: sporadic migraine entry removed (the aura is the CADASIL manifestation); TIA low (stereotyped aura with headache; right putaminal lacune cannot cause aphasia); sporadic SVD very low (NOTCH3); familial early-onset AD very low added; MS very low. |
| E | minor | `ground_truth.key_clinical_evidence` | Two "July 2026 review" / "Tier per" engineering sentences (class D); "triptans relatively contraindicated due to ischaemic stroke risk" generic. | FIXED: rebuilt from the case data. |
| E | minor | `ground_truth.red_herrings` | Entries 2 and 3 with empty `field_path`; entry 3 points at the HPI radiology text that was removed. | FIXED: three red herrings with real paths (family history of dementia, typical-looking aura, MoCA 28/30). |
| A | minor | `fallback_tool_outputs.advanced_imaging` | "MRA" junk fallback (class M). | FIXED: null; kind removed from `metadata.fallback_tool_kinds`. 24-hour Holter, echo, CT and CSF normal fallbacks kept (correct normal reports matching avoided actions). |
| A | minor | avoided actions, stop rule, sequence | `[Charles_2017]` cited for PFO (class N); em dashes; literature in the stop rule, max 0, no constraints. | FIXED: echo rationale without the citation; rationales rewritten for this case; stop rule action-3 and action-5, max 1; soft constraints history before MRI and MRI before NOTCH3. |

## Changes, in one paragraph a physician can read before re-reviewing

A 58-year-old man with three attacks of language aura followed by migrainous headache from age 55, a maternal line with early strokes and dementia and a cousin with NOTCH3 p.Arg182Cys. The HPI no longer quotes the outside MRI report. The pathway is: structured ICHD-3 history (required; criteria A-C met at 4 of 6, criterion D left open because of onset after 50 and the family history, ICHD-3 6.8.1 named), brain MRI compared with the outside study (recommended; anterior temporal pole and external capsule hyperintensities, old right putaminal lacune, no acute infarct or microbleeds), NOTCH3 testing (required; familial pathogenic variant, CADASIL confirmed), neuropsychology (recommended; subcortical-pattern MCI, not dementia; test type now matches), a drug check (recommended; triptans and ergots avoided in CADASIL per EAN 2020, no interaction with his medicines) and an optional literature search with real sources. The genetic counselling "test", the anticoagulation literature and the invented references are gone. Musts: explain CADASIL with migraine aura and MCI; aspirin or NSAID with an antiemetic; raise BP treatment towards below 130/80; clinical genetics for the three adult children; repeat neuropsychology in 12 months. Prohibitions: triptans and ergots; anticoagulation without a compelling indication. In the differential, TIA is low and the sporadic "migraine with aura" entry was removed; familial Alzheimer disease was added as very low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation key `[EAN_CADASIL_2020]` (Mancuso M et al., Eur J Neurol 2020;27:909-927), plan section 5.3; cited by name in rationale, drug output and literature until it exists.

## Open questions for Andrea (judgment calls you could not settle)

- Composition (plan section 6.1): this is a CADASIL case under MIG-AURA. Kept as a mimic case with its own label, per the plan default.
- The EAN 2020 consensus is cited for avoiding triptans and ergots in CADASIL, as the plan directs. I could not open the guideline text in this session; the wording used is "expert consensus advises against vasoconstrictive acute migraine drugs", which matches the plan and the case's previous position. A reviewer should confirm the exact strength of that recommendation.

## Verification

Adversarial verifier, 24 Oct 2026. Read the log, the diff and the whole final case. No reviewer notes exist for MIG-AURA. Checked: the HPI no longer leaks the MRI pattern and the MRI output carries it with technique and comparison; NOTCH3 c.544C>T is p.(Arg182Cys) in exon 4 (correct); `test_type` values agree between criteria and outputs (`genetic_panel:CADASIL`, `neuropsych_battery`); criterion D false agrees with the impression and the label; the drug check stored under `sumatriptan` covers his own medicines and does not echo the expected evidence; musts and prohibitions agree (aspirin or NSAID acute treatment, no triptans or ergots, no anticoagulation without indication, BP towards below 130/80); the differential matches the final evidence (TIA low, sporadic SVD, early-onset AD and MS very low with the excluding data); red herrings point at real fields; avoided actions match the kept normal fallbacks; constraints and stop rule are consistent with the plan (MRI before NOTCH3).
Found: no error requiring a change. The EAN 2020 triptan wording is already hedged as expert consensus, which matches that guideline's evidence level. No edit made. perfect_agent and case_io check clean; leak guard passes.


## Close-out (24 Oct 2026)

Condition close-out (plans/MIG-AURA-decisions.md). Changes and reasons:

- citations [AAN_2000] -> [AHS_neuroimaging_2020] x3, [ICHD_3] x2.
- triptan prohibition and drug-check text: reason restated (old lacunar infarct = label contraindication; CADASIL: not first line, VASCERN 2023), no longer attributed to an EAN 2020 recommendation that could not be verified.
- literature result on triptans in CADASIL and the drug-check rationale rewritten to what VASCERN 2023 says (no evidence contraindicates triptans; not first-line, second or third choice only), source swapped from Mancuso 2020 (its migraine wording could not be checked).
- synonyms unchanged (I67.850, shared with VASC-DEM-P05).
- Citation [AAN_2000] retired: Silberstein 2000 covers treatment, not neuroimaging; imaging statements now cite Evans 2020 [AHS_neuroimaging_2020], test-waste statements [ICHD_3] (diagnosis is clinical).
Checks after the change: `perfect_agent.py` pass, `case_io.py check` clean for the case, `test_case_guards.py -k MIG-AURA-` 60/60.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## Engineering text (25 Oct 2026)

Review-process wording (references to the round's rulings, the round policy file, the criteria packs, and tier markers such as "(optional)" in criterion labels and rationales) is shown to physicians in the review app, so it was rewritten in clinical language. The tier stays in the criterion's `importance` field; scoring is unchanged. `test_case_guards.py::test_no_review_process_text` now fails on any of it.

- criterion `action-1-search-medical-literature` label: "Optional: literature on migraine with aura and its treatment in CADASIL" -> "Literature on migraine with aura and its treatment in CADASIL"
