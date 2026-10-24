# PD-S02
Reviewer status: R1 none, R2 none (PD has no notes file; only the July 2026 tool review, `condition_tool_guidance.yaml` key `parkinsons`) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No physician note exists for PD. The case was corrected against plans/PD.md (classes C1 to C23, per-case entry PD-S02) and the July 2026 tool review (MRI required; ECG, EEG, autonomic and tilt testing removed; labs, neuropsychology and genetics optional and targeted). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | major | `ground_truth.action_criteria[action-3-search-medical-literature]`, `followup_outputs[0]` | Required literature criterion with an exact `query` string; its summary called a "positive DaTscan" a supportive criterion (false, F1) and carried an em dash (C1, ruling 5). | FIXED: criterion and follow-up deleted, removed from the stop rule; initial and fallback literature null. |
| A | major | `action-2-check-drug-interactions`, `followup_outputs[1]` | Required drug check with an exact `drug` string; output said "no clinically significant interactions with ... oxybutynin" and claimed metformin reduces levodopa absorption (false) (C2). | FIXED: `check_drug_interactions {}`, tier `optional`; one stored output `initial_tool_outputs.drug_interactions.general` (oxybutynin C2 sentence plus constipation; amlodipine orthostatic sentence; non-selective MAOI contraindication; metformin and aspirin no relevant interaction; absorption, nausea, sleep attacks, ICD, mirabegron BP warnings); follow-up deleted, fallback null. |
| A | major | `action-1-analyze-brain-mri.alternatives` | `{"contrast": false, "protocol": "standard"}` not matched by a plain MRI order (C5). | FIXED: `analyze_brain_mri {}`; canonical label and rationale; `[Postuma_2015]` only. |
| B | major | `action-1-analyze-brain-mri.expected_evidence` | "Loss of swallow-tail sign supportive when present": the report has no nigrosome finding, and an SWI sign is not a supportive criterion (F1). | FIXED: expected_evidence restates the report (age-appropriate atrophy, Fazekas 1, no infarct or ventriculomegaly, normal midbrain, pons and cerebellum). |
| D | minor | `initial_tool_outputs.mri.additional_observations` | "Patent major intracranial vessels on MRA" on a standard non-angiographic protocol (C12). | FIXED: line deleted; impression given its final period. |
| B | major | `patient.clinical_history.allergies` | "NSAIDs (GI upset)" listed while aspirin 81 mg daily is on the medication list (PATTERNS 3: allergy listed, then the allergen given). | FIXED: "NSAIDs at analgesic doses (GI upset); tolerates low-dose aspirin". |
| C | major | `ground_truth.assessment.required_recommendations`, `key_clinical_evidence[0]` | "Clinically established PD" at a first visit before levodopa (rest tremor is the only supportive criterion) (C6); generic template musts (C16). | FIXED: five musts: C6 probable-PD diagnostic must, canonical levodopa start, agonist caution (age 62), replace oxybutynin by trospium or mirabegron (plan: oxybutynin sentence as a must), PT/OT/SLT referrals tied to her deficits. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Generic prohibitions with an em dash. | FIXED: canonical D2-blocker prohibition; case-specific anticholinergic prohibition (adds to the burden of her bladder antimuscarinic). |
| D | major | `ground_truth.key_clinical_evidence` | Two "July 2026" engineering sentences (C4); "Baseline neuropsych testing" with no such criterion (C15). | FIXED: five case-specific lines. |
| C | minor | `ground_truth.differential` | ET entry with an em dash; MSA did not address her 5-year overactive bladder, the one autonomic feature the case raises (ruling 7). | FIXED: ET, DIP, vascular, MSA and PSP `key_features` rewritten with the excluding exam and MRI data; likelihoods unchanged (already low or very low). |
| C | minor | `ground_truth.avoided_actions` | Generic rationales; no DaTscan, autonomic or tilt guard (C8, 3.3). | FIXED: case-specific rationales; added `avoid-waste-datscan`, `avoid-waste-autonomic-testing`, `avoid-waste-tilt-table`. |
| B | major | `followup_outputs` (missing DaTscan) | No stored DaTscan; the library returns a normal scan, an MDS absolute exclusion of the label (C8). | FIXED: stored C8 report (`request_datscan`): left posterior putamen 1.09, right 1.38 (normal >1.50), caudates 2.28 and 2.47, contralateral to the worse right side. |
| A | minor | `fallback_tool_outputs.ecg`, `.echo`, `metadata.fallback_tool_kinds.echo` | ECG fallback rate 88 against HR 72, "incomplete RBBB" at QRS 97 ms, vague "benign incidental finding"; echo without `echo_type` and vague "near-normal" impression (C17). | FIXED: ECG "Sinus rhythm 72/min, normal axis and intervals, no ST change." (QRS 92 ms); echo `TTE`, EF 60%, concrete normal text, aortic valve structurally normal; fallback kind `normal`. |
| B | minor | `ground_truth.stop_rule` | `max_additional_actions` 0; drug and literature ids listed (C20). | FIXED: MRI only; `max_additional_actions` 2; no sequence constraint (DaTscan waste). |
| E | minor | criterion `rationale`, `citations`; `metadata.difficulty_rationale`, `.revision_reason`, `.last_revised` | Rationale copied from label; bare duplicate keys (C3); shared engineering metadata (C19). | FIXED: distinct rationales, bracketed keys only; case-specific metadata, 2026-10-24. |
| - | check | plan 3.6 | perfect_agent ok; case_io check: no failure names PD-S02; test_case_guards pass; discriminator_defects empty. Routing: DaTscan returns the case report; PSG, battery, orthostatic BP, MIBG, amyloid, FDG return the library (normal, consistent: no dream enactment, MMSE 28/30, no orthostatic symptoms); `drug: levodopa` and `drug: rasagiline` return the case output. | - |

## Changes, in one paragraph a physician can read before re-reviewing

This 62-year-old woman has an 18-month right-predominant tremor-onset parkinsonism (pill-rolling rest tremor, decrement, cogwheel rigidity, micrographia, hypophonia), one near-fall and no red flag. She is now diagnosed as clinically probable PD (rest tremor is her only supportive criterion before levodopa), not "established". The policy is a brain MRI (required, any protocol; the MRA line on a standard study is gone and its expected evidence no longer claims a swallow-tail finding) and an optional medication review whose single stored output now names her oxybutynin (central anticholinergic, worsens constipation) and amlodipine (orthostatic fall), and no longer claims a metformin-levodopa interaction. The literature step is gone; a DaTscan is waste (stored abnormal, left putamen worse). The musts are the probable-PD diagnosis, levodopa titrated to 300 mg/day, the agonist ICD/EDS warning, switching oxybutynin to trospium or mirabegron, and PT/OT/SLT. Her NSAID "allergy" is reworded as intolerance at analgesic doses, since she takes low-dose aspirin.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan R1: `[NICE_NG71]` (levodopa, agonist and therapy musts, DaTscan avoided action) is not yet in the PD criteria pack.

## Open questions for Andrea (judgment calls you could not settle)

- None specific to this case (plan Q1 to Q6 apply).

## Verification
- Checked against the committed rewrite (diff from b8be2153^, field by field), plans/PD.md section 4 entry and classes C1 to C23. No notes file exists for PD, so there is no note id to account for. Tools re-run 24 Oct 2026: perfect_agent ok, case_io check (no failure names the case), test_case_guards pass (leak, followup, banned strings), and a MockServer routing script (MRI or CT, DaTscan, MIBG, amyloid, FDG, PSG, battery, orthostatic BP, labs, ECG, drug check for levodopa and for rasagiline).
- Confirmed every row: literature removed; drug output names oxybutynin (C2 sentence) and amlodipine, no metformin-levodopa claim; MRA line gone; evidence restates the MRI; allergy edit is the only patient change and resolves the NSAID-versus-aspirin contradiction; ECG 72/min, QRS 92 ms, echo `TTE`; DaTscan stored, left putamen worse; stop rule and waste guards as the plan says.
- Checked the oxybutynin must against the drug output and the prohibitions (no contradiction: the anticholinergic prohibition targets trihexyphenidyl and benztropine); MSA entry addresses the 5-year overactive bladder (PMH) without incontinence (HPI). `red_herrings` is empty, as it was before the round; `difficulty_rationale` names the father's ET and the shoulder stiffness as distractors in prose, which is not a contradiction, so no red herring was invented.
- Found nothing to correct. No change made.
