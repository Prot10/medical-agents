# MIG-AURA-P08
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for MIG-AURA) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. July 2026 tool guidance applied through the plan (structured ICHD-3 history required; echo kept here for cardiomyopathy screening). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | blocker | `patient`, `initial_tool_outputs.mri` | The data did not support MELAS (plan P08): only brief fully reversible attacks, a normal MRI, normal examination; the label says stroke-like episodes. | FIXED (data, not label): HPI adds a latest episode 10 days ago (hours of onset, left arm weakness, left visual loss, headache with vomiting, confusion; arm recovered over 4 days, field loss persists); chief complaint, `neurological_exam.cranial_nerves`, `mental_status`, `physical_exam.general` and `.neurological` now record a left inferior homonymous quadrantanopia and slight slowing; MRI shows a right parieto-occipital cortical lesion crossing MCA and PCA territories with gyral swelling and mostly normal to increased ADC. |
| A | major | `initial_tool_outputs.clinical_assessment` | Template (class A), "6 of 6" with succession true although only motor symptoms are described. | FIXED: brief attacks 4 of 6 and ICHD-3 1.2.3 B not met (motor only); latest episode not an aura (persistent); systemic features, family history, medicines, examination, red flags; criterion D false. |
| D | major | `initial_tool_outputs.labs` | The initial labs carried the m.3243A>G result, so ordering a lactate returned the genetic diagnosis; values written as strings with ranges in the value; L/P ratio "20 (ref <20)" flagged abnormal. | FIXED: initial labs: lactate 2.8 (kept), pyruvate 0.10 (normal), L/P ratio 28 (ref 10-25), CK 182 (kept), fasting glucose and HbA1c normal, real units and ranges. mtDNA moved to its own criterion and follow-ups (below). |
| C | major | `ground_truth.action_criteria` (new `action-mtdna-test`), `followup_outputs[1]`, `[2]` | No criterion for the m.3243A>G test although a must demanded it (class J). | FIXED: required criterion with alternatives `interpret_labs` `m3243A_G_mtDNA` and `order_specialized_test` `genetic_panel:mitochondrial`; two follow-ups with the same result (urine 62%, blood 28%, sample choice stated). The labs follow-up also repeats the metabolic panel so a combined order is answered in full (checked). |
| D | major | `followup_outputs[0]` (MRS) | "Elevated lactate peak in affected territory, supports MELAS" (diagnosis named; one line). | FIXED: technique, voxels, lactate doublet in lesion, normal-appearing cortex and ventricular CSF, NAA/Cr values, numbered impression without the disease name. |
| B | minor | `followup_outputs[3]` (echo) | One text blob, empty structured fields, no `echo_type` (the TTE criterion relied on prose). | FIXED: `echo_type: TTE`, chambers, valves, EF 60, wall motion, findings and numbered impression; same findings (IVSd 12 mm, grade I diastolic dysfunction). |
| C | major | `ground_truth.action_criteria` (new `action-ecg`), `initial_tool_outputs.ecg` | ECG was a must with no criterion (class J); plan P08 adds a recommended ECG. | FIXED: recommended `analyze_ecg`; ECG: sinus rhythm, LVH voltage, no pre-excitation or conduction block. ECG must deleted. |
| C | major | `followup_outputs` (two literature searches), `initial_tool_outputs.literature_search` | Two empty literature follow-ups; initial literature block was the template whose text equals the expected evidence (guard leak). | FIXED: both deleted, initial block null; one literature follow-up with real consensus sources (Parikh MMS 2017; Ng 2019) and ICHD-3 1.2.3, last. |
| C | major | `followup_outputs` (drug check), `action-2` | `{"context": ...}` criterion (unreachable); "triptans CONTRAINDICATED... worsens stroke-like episodes" stated as fact; "formulary_status: contraindicated"; `[Holland_2012]` cited for arginine. | FIXED: stored check under `valproate` in `initial_tool_outputs.drug_interactions` (any drug): valproate and metformin avoided, topiramate caution, propofol caution, triptans avoided on expert opinion, alternatives levetiracetam or lacosamide. Recommended (no antiseizure or preventive in the plan, plan P08 rule); alternatives valproate, sodium valproate, topiramate, levetiracetam, metformin, sumatriptan. |
| C | minor | `ground_truth.action_criteria` (`action-4`, `-5`, `-6`, `-7`, `-1`) | MRI pinned `contrast: false, protocol: standard`; labs optional with generic text; labels equal rationales; `[AAN_2000]` and `ICHD-3; NICE` citations. | FIXED: MRI `{}` required; labs recommended (`lactate` or `CK`); echo and MRS labels and evidence from the case; literature optional `{}` last. |
| C | major | `ground_truth.assessment.required_recommendations` | Musts were tests (mtDNA, echo and ECG); "avoid triptans..." duplicated prohibitions; L-arginine without its evidence status. | FIXED: seven musts: explain MELAS; emergency plan for stroke-like episodes with arginine as MMS 2017 consensus and its disputed evidence (Ng 2019); cardiology with yearly ECG and echo; audiology; yearly diabetes screen and no metformin; clinical genetics for maternal inheritance and relatives; visual field rehabilitation. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Generic wording. | FIXED: valproate and metformin; triptans and ergots after a stroke-like episode (expert opinion); keeping the hemiplegic migraine label. |
| C | major | `ground_truth.differential` | Sporadic hemiplegic migraine `high` while the label is MELAS (class F); "cardioembolic TIA" with no cardiac work-up of that kind. | FIXED: sporadic HM low, familial HM very low, arterial ischaemic stroke low, other m.3243A>G phenotype (MIDD) low, each with the excluding data; cardioembolic TIA removed. |
| E | minor | `ground_truth.key_clinical_evidence` | Three "July 2026 review" sentences (class D). | FIXED: rebuilt from the case data. |
| E | minor | `ground_truth.red_herrings` | Entries 2 and 3 had empty paths; entry 3 was self-contradictory. | FIXED: two red herrings (chief complaint label; HPI brief motor attacks). |
| B | minor | `fallback_tool_outputs.ct` | Fallback CT reported a normal brain with a "benign granuloma", contradicting the MRI lesion. | FIXED: CT fallback shows the right parieto-occipital hypodensity and bilateral pallidal calcification; kind `case_specific`. MRA fallback set null (class M). Holter and CSF fallbacks kept. |
| A | minor | stop rule, sequence, metadata | Literature in the stop rule, max 0, no constraints; `metadata.case_body_concerns` said analyze_ecg was dropped. | FIXED: stop rule history, MRI, mtDNA, echo; max 1; soft constraints history before MRI and MRI before mtDNA; concern removed (ECG now in the case); `condition_name` updated. |

## Changes, in one paragraph a physician can read before re-reviewing

A 29-year-old woman with short stature, hearing loss and a mother with m.3243A>G MELAS, labelled hemiplegic migraine. The case now has a latest episode that lasted days and left a left inferior homonymous quadrantanopia, so the data support the MELAS label. The structured history shows the brief attacks are motor only and do not meet ICHD-3 1.2.3. The pathway: history; brain MRI (right parieto-occipital cortical lesion crossing MCA and PCA territories, gyral swelling, mostly normal to increased ADC); MR spectroscopy (lactate in the lesion, in normal-appearing cortex and in CSF); blood lactate 2.8 mmol/L with L/P ratio 28 and CK 182; m.3243A>G testing (new required criterion: 62% urine, 28% blood); TTE (mild concentric LVH, grade I diastolic dysfunction); ECG (new, LVH voltage, no pre-excitation); drug check (recommended: valproate and metformin avoided, topiramate caution); optional literature with real consensus sources. Ordering a lactate no longer returns the genetic result. Musts: explain MELAS; an emergency plan for stroke-like episodes (L-arginine as MMS 2017 consensus with low evidence, not endorsed by the UK consensus); cardiology surveillance; audiology; diabetes screening without metformin; clinical genetics; visual rehabilitation. Hemiplegic migraine is now low in the differential.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation key `[MMS_2017]` (Parikh S et al., Genet Med 2017;19(12)) and a key for Ng YS et al., Wellcome Open Res 2019;4:201; cited by name until they exist.
- Guidance claims (plan 5.5): P08 gains ECG (recommended) and keeps echo.

## Open questions for Andrea (judgment calls you could not settle)

- Composition (plan section 6.1): MELAS case under MIG-AURA, kept as a mimic case per the plan default.
- Triptan avoidance in MELAS is kept as a prohibition on expert opinion, as the case and plan had it; I found no guideline that states a formal contraindication and the text says so. A reviewer may prefer it as a caution rather than a prohibition.
- Lactate kept at the stored 2.8 mmol/L (raised) instead of the plan's example 4.1 mmol/L: the stored value already supports the label, and changing it would be churn.

## Verification

Adversarial verifier, 24 Oct 2026. Read the log, the diff and the whole final case. No reviewer notes exist for MIG-AURA. Checked: the new latest episode, examination (left inferior homonymous quadrantanopia), MRI (right parieto-occipital, crossing MCA and PCA territories) and CT fallback agree on side and site; lactate to pyruvate arithmetic (2.8 / 0.10 = 28) and `is_abnormal` flags against the ranges are right; heteroplasmy values agree across the labs follow-up, the genetic report, expected evidence and key evidence; the initial labs no longer return the genetic result; ICHD-3 1.2.3 B (motor plus visual, sensory or speech) is stated correctly and the motor-only attacks fail it; echo and ECG values agree with their criteria (IVSd 12 mm, Sokolow-Lyon 38 mm); valproate, metformin and topiramate cautions agree with the prohibitions; the differential matches the final evidence; stop rule and MRI-before-mtDNA constraint are consistent.
Found and fixed:
- `ground_truth.assessment.required_recommendations[1]` called Ng 2019 the "UK consensus"; it is an international consensus. Now "the 2019 international consensus on stroke-like episodes (Ng YS et al., Wellcome Open Res 2019) found the evidence insufficient to recommend it", which also matches the literature output.
- `initial_tool_outputs.mri.additional_observations`: the CT fallback reports bilateral pallidal calcification but the MRI with SWI was silent on it. Added "Symmetric susceptibility signal in both globi pallidi, consistent with mineralisation" to the SWI line so the two reports agree.
- `metadata.difficulty_description` said "triptans must be stopped" although she takes no triptan; now "triptans and valproate are avoided".
perfect_agent and case_io check clean; leak guard passes.


## Close-out (24 Oct 2026)

Condition close-out (plans/MIG-AURA-decisions.md). Changes and reasons:

- citations [AAN_2000] -> [AHS_neuroimaging_2020] x1, [ICHD_3] x2.
- synonyms unchanged (E88.41).
- Citation [AAN_2000] retired: Silberstein 2000 covers treatment, not neuroimaging; imaging statements now cite Evans 2020 [AHS_neuroimaging_2020], test-waste statements [ICHD_3] (diagnosis is clinical).
Checks after the change: `perfect_agent.py` pass, `case_io.py check` clean for the case, `test_case_guards.py -k MIG-AURA-` 60/60.

## Engineering text (25 Oct 2026)

Review-process wording (references to the round's rulings, the round policy file, the criteria packs, and tier markers such as "(optional)" in criterion labels and rationales) is shown to physicians in the review app, so it was rewritten in clinical language. The tier stays in the criterion's `importance` field; scoring is unchanged. `test_case_guards.py::test_no_review_process_text` now fails on any of it.

- criterion `action-1-search-medical-literature` label: "Optional: literature on mitochondrial stroke-like episodes and hemiplegic migraine criteria" -> "Literature on mitochondrial stroke-like episodes and hemiplegic migraine criteria"
