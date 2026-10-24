# PD-S03
Reviewer status: R1 none, R2 none (PD has no notes file; only the July 2026 tool review, `condition_tool_guidance.yaml` key `parkinsons`) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No physician note exists for PD. The case was corrected against plans/PD.md (classes C1 to C23, per-case entry PD-S03) and the July 2026 tool review (MRI required; ECG, EEG, autonomic and tilt testing removed; labs, neuropsychology and genetics optional and targeted). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | major | `ground_truth.action_criteria[action-3-search-medical-literature]`, `followup_outputs[1]` | Required literature criterion with an exact `query` string (C1, ruling 5). | FIXED: criterion and follow-up deleted, removed from the stop rule; initial and fallback literature null. |
| A | major | `action-2-check-drug-interactions`, `followup_outputs[0]` | Required drug check with an exact `drug` string; output said "no significant interactions with amlodipine, metformin, tamsulosin, aspirin, or naproxen" while warning of orthostasis with amlodipine and tamsulosin, and missed naproxen with aspirin (C2). | FIXED: `check_drug_interactions {}`, tier `optional`; one stored output `initial_tool_outputs.drug_interactions.general` (tamsulosin C2 sentence; amlodipine; naproxen with low-dose aspirin: GI bleeding and reduced antiplatelet effect, acetaminophen preferred; non-selective MAOI contraindication; metformin no relevant interaction; nausea, protein, sleep attacks, ICD warnings; agonists flagged for hallucinations after 70); follow-up deleted, fallback null. |
| A | major | `action-1-analyze-brain-mri.alternatives` | `{"contrast": false, "protocol": "standard"}` not matched by a plain MRI order (C5). | FIXED: `analyze_brain_mri {}`; canonical label and rationale; `[Postuma_2015]` only. |
| B | major | `action-1-analyze-brain-mri.expected_evidence` | "SWI may show loss of swallow-tail sign": no nigrosome finding in the report (C12). | FIXED: expected_evidence restates the report. |
| D | minor | `initial_tool_outputs.mri.additional_observations` | "Patent major intracranial vessels on MRA" on a standard protocol (C12). | FIXED: deleted; impression given its final period. |
| C | major | `followup_outputs` PSG (`request_optional_psg_for_reported_dream_enactment`) | Auto-generated "Abnormal values: ..." impression with em dashes; no RSWA quantification, REM latency or SpO2 nadir; REM 18% flagged abnormal against an adult range at 71 (C10). | FIXED: full report (TST 342 min, efficiency 79%, REM latency 94 min, REM 18% against an age 70+ range, RSWA 36% of REM epochs against the SINBAR 27% threshold, two video episodes of limb jerking and arm extension, AHI 3.9, SpO2 nadir 91%, PLMI 13) and the C10 impression; trigger kept (routes by `test_type`). Criterion stays `optional`, with a case-specific rationale and expected_evidence, citation `[Berg_2015]` (was `[NICE_NG71]` plus a bare key). |
| B | major | `followup_outputs` (missing battery) | Exam MoCA 27/30, but an ordered battery would return the library's MoCA 28/30 (C9). | FIXED: stored battery (`request_neuropsych_testing`, `neuropsych_battery`) with MoCA 27/30, all domains within normal limits, low-average phonemic fluency (the letter-fluency point lost on the MoCA), GDS 2/15; no criterion. |
| B | major | `followup_outputs` (missing DaTscan) | No stored DaTscan; the library returns a normal scan, an MDS absolute exclusion (C8). | FIXED: stored C8 report: left posterior putamen 1.21, right 1.46 (normal >1.50), caudates 2.33 and 2.49, contralateral to the right-sided signs. |
| C | major | `ground_truth.assessment.required_recommendations`, `key_clinical_evidence[0]` | "Clinically established PD" at a first visit before levodopa (C6); generic template musts (C16). | FIXED: five musts: C6 probable-PD diagnostic must, canonical levodopa start, lying and standing BP during titration (tamsulosin, amlodipine), RBD bedroom safety with melatonin preferred over clonazepam at 71, PT/OT/SLT. The agonist caution must is not added (age 71, levodopa first). |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Generic prohibitions with an em dash. | FIXED: canonical D2-blocker prohibition; case-specific anticholinergic prohibition (age, BPH). |
| D | major | `ground_truth.key_clinical_evidence` | Two "July 2026" engineering sentences (C4). | FIXED: six case-specific lines. |
| C | minor | `ground_truth.differential` | Dream enactment with parkinsonism raises DLB, which was not addressed (ruling 7); key_features generic. | FIXED: DLB added `very_low` (no dementia, fluctuations or hallucinations; MoCA 27); ET, DIP, vascular, MSA, PSP `key_features` rewritten with the excluding data. |
| C | minor | `patient.neurological_exam.sensory` | Reduced great-toe vibration called "likely age-related" in a man with 8 years of type 2 diabetes and 1+ ankle reflexes: the exam attributed a finding that may be a mild length-dependent neuropathy. | FIXED: attribution removed ("Mildly reduced vibratory sense at both great toes."). |
| C | minor | `ground_truth.avoided_actions` | Generic rationales; no DaTscan, autonomic or tilt guard (C8, 3.3). | FIXED: case-specific rationales (EEG: nocturnal episode is for video-PSG); added `avoid-waste-datscan`, `avoid-waste-autonomic-testing`, `avoid-waste-tilt-table`. |
| A | minor | `fallback_tool_outputs.ecg`, `.echo` | ECG fallback with "incomplete RBBB" at QRS 89 ms and vague text, rate 71 against HR 70; echo without `echo_type` (C17). | FIXED: ECG "Sinus rhythm 70/min, normal axis and intervals, no ST change."; echo `TTE`, EF 59%, concrete normal text. |
| C | minor | `metadata.key_educational_points[0]` | Listed postural instability as a cardinal feature for the diagnosis; MDS 2015 removed it from the core criteria. | FIXED: "bradykinesia with rest tremor, rigidity or both (MDS 2015; postural instability is no longer a core criterion)". |
| B | minor | `ground_truth.stop_rule` | `max_additional_actions` 0; drug and literature ids (C20). | FIXED: MRI only; 2; no sequence constraint (DaTscan waste). |
| E | minor | criterion `rationale`, `citations`; `metadata.difficulty_rationale`, `.revision_reason`, `.last_revised` | Rationale copied from label, bare duplicate keys (C3); shared engineering metadata (C19). | FIXED. |
| - | check | plan 3.6 | perfect_agent ok; case_io check: no failure names PD-S03; test_case_guards pass; discriminator_defects empty. Routing: DaTscan, PSG and battery return the case reports; MIBG, amyloid, FDG and orthostatic BP return the library; `drug: levodopa` and `drug: rasagiline` return the case output. | - |

## Changes, in one paragraph a physician can read before re-reviewing

This 71-year-old man has a 2.5-year right-sided tremor-onset parkinsonism (pill-rolling rest tremor, decrement, cogwheel rigidity at wrist and ankle, micrographia, hypophonia), one near-fall, constipation and one witnessed episode of punching the air while dreaming. He is now clinically probable PD (rest tremor the only supportive criterion before levodopa), not "established". The policy is a brain MRI (required, any protocol; MRA line removed) and an optional video-PSG for the dream enactment, whose report is now a full study (RSWA 36% of REM epochs with limb jerking on video, no sleep apnea, PLMI 13) rather than an "Abnormal values" list; the medication review is optional and its one output now names tamsulosin and amlodipine (orthostasis) and naproxen with aspirin (bleeding). The literature step is gone; a DaTscan is waste (stored abnormal, left putamen worse); a stored battery matches his MoCA 27. The musts are the probable-PD diagnosis, levodopa titrated to 300 mg/day, lying and standing BP during titration, RBD bedroom safety (melatonin rather than clonazepam) and PT/OT/SLT. DLB is added at very low likelihood.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan R1: `[NICE_NG71]` (levodopa and therapy musts, DaTscan avoided action) is not yet in the PD criteria pack.

## Open questions for Andrea (judgment calls you could not settle)

- None specific to this case (plan Q1 to Q6 apply).
