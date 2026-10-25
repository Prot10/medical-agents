# PD-P03
Reviewer status: R1 none, R2 none (PD has no notes file; only the July 2026 tool review, `condition_tool_guidance.yaml` key `parkinsons`) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No physician note exists for PD. The case was corrected against plan PD (classes C1 to C23, per-case entry PD-P03) and the July 2026 tool review (MRI required, ECG and EEG removed, labs targeted, autonomic and tilt testing removed, neuropsychology optional). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `initial_tool_outputs.literature_search`, criterion `action-3-search-medical-literature` | Recommended literature criterion with an exact `query`; stored output repeated its expected evidence (leak test failed, C1). | FIXED: criterion deleted; initial and fallback literature outputs null. |
| D | major | `initial_tool_outputs.drug_interactions.general` | Empty block whose summary was the criterion's expected evidence ("document poor levodopa response as supportive of PSP"), a diagnostic statement in a drug check (C2). | FIXED: rebuilt from her own medicines: amlodipine with levodopa (additive hypotension, lying and standing BP at each step), calcium carbonate with levothyroxine (separate by 4 hours), sedative and anticholinergic fall-risk warning. Fallback drug output null. |
| A | major | `ground_truth.action_criteria[action-2-check-drug-interactions]` | `recommended` with an exact `drug` string ("carbidopa-levodopa trial reassessment") no agent can match (C2). | FIXED: `check_drug_interactions {}`, `optional` (plan C2: no dopamine blocker, no management-changing pair), moved last. |
| A | major | `ground_truth.action_criteria[action-1-analyze-brain-mri]` | Required `{"contrast": false, "protocol": "standard"}` (C5); rationale copied the PD label (C3). | FIXED: `analyze_brain_mri {}`; PSP-specific rationale [Hoglinger_2017]; expected evidence restates the report. |
| B | major | `patient.history_present_illness`, `.clinical_history.medications[4]`, `.neurological_exam.additional` | "25/250 TID (600 mg/day)" is 750 mg/day; the medication list still read 25/100 TID (C18). | FIXED: "two tablets of 25/100 three times daily (600 mg/day levodopa)" in the HPI and the medication list; the duplicated trial history removed from the exam. |
| B | major | `patient.neurological_exam.mental_status` | MMSE losses did not sum to 25 (3 serial-seven errors scored as 2 points; the date error not counted; a sentence of 3 words scored as a loss); MoCA items as listed summed to 21, not 20. | FIXED: MMSE serial sevens 2 errors (2 points), recall 1, date 1, pentagons 1 (25/30); MoCA itemised to 20/30 (visuospatial/executive 3/5, naming 3/3, attention 5/6, language 2/3, abstraction 0/2, recall 2/5, orientation 5/6), consistent with the FAS of 8 words. |
| D | minor | `patient.neurological_exam.cranial_nerves`, `.gait`, `.motor`, `.mental_status` | Examiner teaching comparisons in the patient block ("opposite of PD's flexed posture", "distinct from PD", "different from the hypophonic speech of PD", "confirms the gaze palsy is SUPRANUCLEAR"); oculocephalic test described as head rotation for vertical gaze. | FIXED: findings kept, comparisons with PD removed; oculocephalic manoeuvre with passive flexion and extension. |
| C | minor | `initial_tool_outputs.mri` | "post-gadolinium" on a non-contrast study (C12); Fazekas grade filed under the midbrain; pontine area 3.2 cm2 called normal (low for an adult) and a "midbrain-to-pons ratio" of 0.47 with the 0.52 cut-off, which is the diameter ratio (Massey 2013), not the area ratio; teaching prose in the impression. | FIXED: gadolinium line deleted; one finding per structure (white matter separate); midbrain area 0.62 cm2 (reduced), pontine area 4.8 cm2 (normal), "midbrain-to-pons diameter ratio 0.47 (normal above 0.52)"; numbered impression. |
| D | major | `followup_outputs[0]` neuropsych battery | "Abnormal values" impression with inverted flags (Stroop z -2.8 "(H)", FAB 8/18 "(H)") (C10). | FIXED: C10 impression (dysexecutive profile of frontal-subcortical type, preserved recall, naming and visuoconstruction; apathy scale elevated); trigger `request_neuropsych_testing`. |
| B | major | `followup_outputs` (no DaTscan) | The library DaTscan is normal, an absolute exclusion that is false in PSP (C8). | FIXED: symmetric PSP/MSA report stored (`request_datscan`, putamen SBR 1.0/1.1, caudate 1.6/1.7); DaTscan `waste` in `avoided_actions` ("does not separate PD from MSA or PSP" [Marshall_2009]). |
| C | major | `ground_truth.assessment.required_recommendations` | Generic PD musts ("Apply MDS 2015 PD criteria", temporal sequence, medication list) for a PSP label (C7, C16). | FIXED: probable PSP-RS (O1 with P1, MDS 2017); SLT swallowing assessment; fall prevention with bone-protection review; completion of the levodopa trial up to 1000 mg/day as tolerated, then taper; prognosis, advance care planning and palliative care. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Four items, overlapping, with pimavanserin (PD-psychosis licence). | FIXED: canonical D2-blocker prohibition and one sedative/anticholinergic fall-risk prohibition. |
| C | major | `ground_truth.differential[0]` | PD `moderate` after an exam that meets an MDS absolute exclusion (C13). | FIXED: PD `low` with the excluding features; bvFTD added `low` (the case raises personality change); MSA, DLB, CBS, vascular with case-specific features. |
| C | major | `ground_truth.red_herrings[0].correct_interpretation` | Called backward falls an "absolute exclusion" for established PD; falls are a PSP core feature (P1), not an MDS exclusion. | FIXED: rewritten; second red herring (falls blamed on amlodipine-related orthostatic hypotension) added from the HPI. |
| E | minor | `ground_truth.key_clinical_evidence` | Two "July 2026" engineering sentences (C4); generic hallmarks list. | FIXED: six case-specific items with O1, P1, levodopa resistance, frontal features, MRI figures, priorities. |
| A | minor | `ground_truth.avoided_actions` | Generic rationales; no autonomic, tilt or DaTscan guard (plan 3.3, C8). | FIXED: CSF, echo, monitoring rationales case-specific; DaTscan, autonomic testing and tilt table `waste` added. |
| B | minor | `ground_truth.stop_rule` | `max_additional_actions` 0 (C20). | FIXED: 2; required list MRI only; no sequence constraint (DaTscan is waste). |
| A | minor | `fallback_tool_outputs.advanced_imaging`, `.echo` | FDG fallback `modality` "FDG-PET" and an Alzheimer comparison (C11, C17); echo without `echo_type`. | FIXED: `FDG_PET`, regional pattern only; echo `TTE` with concrete findings. |
| E | minor | `metadata` | Stale citation gap (Gilman 2008), "1 required tool actions after the independent reviewer audit", removed fallback kinds. | FIXED: citation gap [Hoglinger_2017]; difficulty and revision fields rewritten; `last_revised` 2026-10-24. |
| - | check | plan 3.6 | perfect_agent ok (MRI `<- ?` is the dump-comparison label of the initial MRI; the routing probe confirms the case MRI answers); case_io check clean; test_case_guards pass; routing: DaTscan and neuropsych from the case, FDG from the case fallback, MIBG, PSG, amyloid and orthostatic from the library (normal MIBG and PSG fit PSP with no dream enactment; the exam orthostatic figures are normal). Pre-existing em dashes in the unedited HPI sentences and PMH left. | - |

## Changes, in one paragraph a physician can read before re-reviewing

The levodopa trial now reads two tablets of 25/100 three times daily (600 mg/day) in the HPI and the medication list; the old "25/250 TID" was 750 mg/day. The MMSE (25/30) and MoCA (20/30) item scores now sum to their totals. The exam keeps every finding but no longer argues against PD in the examiner's voice. The MRI report is restructured (midbrain area 0.62 cm2, midbrain-to-pons diameter ratio 0.47, pons and putamina preserved, Fazekas 1 separately). The literature step is gone; the medication review is optional and names amlodipine with levodopa and calcium with levothyroxine. A symmetric abnormal DaTscan is stored and ordering it is waste. Policy: MRI required, neuropsychology and medication review optional. Musts: probable PSP-RS by MDS 2017 (O1 with P1), SLT swallowing assessment, fall prevention with bone protection, completion of the levodopa trial up to 1000 mg/day as tolerated then taper, and advance care planning. PD and the other mimics are low in the differential; a second red herring records the PCP's amlodipine explanation of the falls.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan R1: `[Hoglinger_2017]` used per the plan; not yet in the PD pack.
- Plan R5: the library DaTscan default is normal, an MDS absolute exclusion that is false in PSP; this case now stores its own symmetric report.

## Open questions for Andrea (judgment calls you could not settle)

- None specific to this case (plan Q1 applies: PSP kept under the PD prefix). The must to complete the levodopa trial up to 1000 mg/day is a clinical judgment (many movement-disorder services give PSP-RS such a trial before stopping levodopa); it is phrased "up to 1000 mg/day as tolerated" so that the dose ceiling is checkable without forcing a dose the patient cannot tolerate.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the checkpoint diff (b8be2153) and the whole final case. Checked: levodopa 600 mg/day consistent in HPI and medication list; MMSE 25 and MoCA 20 (3+3+5+2+0+2+5) sum, FAS 8 consistent with 3 F-words; MRI figures (midbrain 0.62 cm2, pons 4.8 cm2, diameter ratio 0.47) coherent with PSP; symmetric DaTscan stored and waste; FDG fallback `FDG_PET` with pattern only; drug output (amlodipine with levodopa, calcium with levothyroxine) correct; routing serves the case DaTscan, battery and FDG, and library MIBG, PSG and orthostatic reports that fit the case.
Found and fixed:
- C major, `ground_truth.assessment.required_recommendations[0]` and `ground_truth.key_clinical_evidence[2]`: "levodopa resistance" was counted as a supportive feature after 600 mg/day for 4 weeks, while MDS 2017 [Hoglinger_2017] defines levodopa resistance only after at least 1000 mg/day (if tolerated) for at least a month, and must [3] of the same case asks to complete that trial. Rewritten: dysarthria and dysphagia are the supportive clinical clues; levodopa resistance cannot yet be stated.
- B minor, `ground_truth.differential` (DLB) `key_features`: claimed "no dream enactment", which the case never documents (no sleep history). Now "No visual hallucinations or cognitive fluctuations; the vertical supranuclear gaze palsy and early unprovoked backward falls are not DLB features".
After the edit: perfect_agent ok; case_io check clean for PD-P03; test_case_guards pass; discriminator_defects empty.

## Close-out (24 Oct 2026)

Decisions in `plans/PD-decisions.md`.

- Stays in condition parkinsons as a PD-mimic case (ruling 3); `metadata.case_body_concerns` and `citation_gap` cleared (`[Hoglinger_2017]` is in the PD pack). Labels and code unchanged (G23.1). No PD label or G20 code is accepted.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: levodopa_challenge}`: MDS-UPDRS III 41/132 OFF, 38/132 ON (7%) (fallback_tool_outputs.clinical_assessment). Why: rule 3: the stored exam documents parkinsonism; the library reports MDS-UPDRS III 3/132 with no parkinsonian signs; PSP on 600 mg/day levodopa with no benefit.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}`: TUG 21.4 s, 10 m 0.68 m/s, Berg 34/56 (followup request_gait_and_balance_timed). Why: rule 3: the stored gait exam (arm swing, stride, turns, pull test) is abnormal; the library reports a normal gait, turns in 3 steps and Berg 56/56.
- `perform_clinical_assessment {assessment_type: cognitive_screen}`: MoCA 20/30 as in the exam (followup request_cognitive_screen). Why: rule 3: the stored exam records this MoCA and its items; the library reports MoCA 28/30 with other items.
- `perform_clinical_assessment {assessment_type: orthostatic_blood_pressure}`: 148/88 supine, 142/84 at 3 min (as in the exam) (followup request_orthostatic_blood_pressure). Why: rule 3: the stored exam records orthostatic vitals; the library reports supine 128/78 and other numbers.
- `order_specialized_test {test_type: speech_language_evaluation}`: spastic dysarthria (70 dB SPL), no aphasia (fallback_tool_outputs.specialized_test). Why: rule 3: the stored exam records spastic dysarthria; the library reports no motor speech disorder.

Checks: `perfect_agent.py` 30/30 PD pass; `test_case_guards.py -k PD-` and `pytest agent-platform/tests -k PD-` 300 passed (`test_grpo_rollout.py` not collected: training extra not installed); every criterion's served output unchanged (snapshot before/after); synonym guard 0 changes; no new report repeats a 60-character window of any `expected_evidence`; every listed term is answered without the library.
