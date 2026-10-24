# PD-S04
Reviewer status: R1 none, R2 none (PD has no notes file; only the July 2026 tool review, `condition_tool_guidance.yaml` key `parkinsons`) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No physician note exists for PD. The case was corrected against plans/PD.md (classes C1 to C23, per-case entry PD-S04) and the July 2026 tool review (MRI required; ECG, EEG, autonomic and tilt testing removed; labs, neuropsychology and genetics optional and targeted). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | major | `ground_truth.action_criteria[action-3-search-medical-literature]`, `followup_outputs[1]` | Required literature criterion with an exact `query` string (C1, ruling 5). | FIXED: criterion and follow-up deleted, removed from the stop rule; initial and fallback literature null. |
| A | major | `action-2-check-drug-interactions`, `followup_outputs[0]` | Required drug check with an exact `drug` string; output said "no significant interactions with tamsulosin" and then warned of additive hypotension; em dashes (C2). | FIXED: `check_drug_interactions {}`, tier `optional`; one stored output `initial_tool_outputs.drug_interactions.general` (tamsulosin C2 sentence; amlodipine; non-selective MAOI contraindication; acetaminophen no relevant interaction; nausea, protein, sleep attacks and driving, ICD, hallucination warnings); follow-up deleted, fallback null. |
| A | major | `action-1-analyze-brain-mri.alternatives` | `{"contrast": false, "protocol": "standard"}` not matched by a plain MRI order (C5). | FIXED: `analyze_brain_mri {}`; canonical label and rationale; `[Postuma_2015]` only; expected_evidence restates the report. |
| B | major | `initial_tool_outputs.mri.additional_observations` | "No ... pathological enhancement after gadolinium administration" on a non-contrast study (C12); "appropriate for age and history of hypertension" brings clinical history into the report (style guide prohibition 1). | FIXED: "No mass lesion"; "Mild chronic small vessel ischemic changes appropriate for age"; impression given its final period. |
| B | major | `followup_outputs` (missing battery) | Exam MoCA 27/30, but an ordered battery would return the library's MoCA 28/30 (C9). | FIXED: stored battery (`request_neuropsych_testing`) with MoCA 27/30, all domains within normal limits, low-average Trail Making B, GDS 4/15; no criterion. |
| B | major | `followup_outputs` (missing DaTscan) | No stored DaTscan; the library returns a normal scan, an MDS absolute exclusion (C8). | FIXED: stored C8 report: left posterior putamen 1.04, right 1.35 (normal >1.50), caudates 2.21 and 2.44, contralateral to the worse right side. |
| C | major | `ground_truth.assessment.required_recommendations`, `key_clinical_evidence[0]` | "Clinically established PD" at a first visit before levodopa; his smell loss is self-reported, not a validated test, so rest tremor is the only supportive criterion (C6); generic template musts (C16). | FIXED: five musts: C6 probable-PD diagnostic must (noting the self-reported smell loss), canonical levodopa start with lying and standing BP at each step (tamsulosin, amlodipine), agonist caution (age 67), driving (wife reports slower reactions at intersections; formal assessment; no driving with sudden sleep onset), PT/OT/SLT. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Generic prohibitions with an em dash. | FIXED: canonical D2-blocker prohibition; case-specific anticholinergic prohibition (age, BPH). |
| D | major | `ground_truth.key_clinical_evidence` | Two "July 2026" engineering sentences (C4). | FIXED: five case-specific lines. |
| C | minor | `ground_truth.differential` | Generic key_features; the mild right postural tremor and the mother's undiagnosed "shaking" not addressed under ET. | FIXED: ET, DIP, vascular, MSA, DLB `key_features` rewritten with the excluding data; likelihoods unchanged (already low or very low). |
| B | minor | `ground_truth.red_herrings` | Empty, although the family history carries a real distractor. | FIXED: mother's uncharacterized late-life tremor (`family_history[1]`) as an ET anchor, with its interpretation. |
| C | minor | `ground_truth.avoided_actions` | Generic rationales; no DaTscan, autonomic or tilt guard (C8, 3.3). | FIXED: case-specific rationales; added `avoid-waste-datscan`, `avoid-waste-autonomic-testing`, `avoid-waste-tilt-table`. |
| A | minor | `fallback_tool_outputs.ecg`, `.echo` | ECG fallback rate 82 against HR 69, "borderline left-axis deviation" with a normal axis field, vague impression; echo without `echo_type` (C17). | FIXED: ECG "Sinus rhythm 69/min, normal axis and intervals, no ST change."; echo `TTE`, EF 58%, concrete normal text. |
| B | minor | `ground_truth.stop_rule` | `max_additional_actions` 0; drug and literature ids (C20). | FIXED: MRI only; 2; no sequence constraint (DaTscan waste). |
| E | minor | criterion `rationale`, `citations`; `metadata.difficulty_rationale`, `.revision_reason`, `.last_revised` | Rationale copied from label, bare duplicate keys (C3); shared engineering metadata (C19). | FIXED. |
| - | check | plan 3.6 | perfect_agent ok; case_io check: no failure names PD-S04; test_case_guards pass; discriminator_defects empty. Routing: DaTscan and battery return the case reports; PSG returns the library normal (he denies dream enactment), MIBG, amyloid, FDG and orthostatic BP the library; `drug: levodopa` and `drug: rasagiline` return the case output. | - |

## Changes, in one paragraph a physician can read before re-reviewing

This 67-year-old man has a 2.5-year right-predominant tremor-onset parkinsonism (pill-rolling rest tremor with re-emergence, decrement, cogwheel rigidity, micrographia, hypophonia), no falls, constipation and self-reported smell loss. He is now clinically probable PD, not "established": the smell loss is not a validated test, so rest tremor is his only supportive criterion until levodopa is tried. The policy is a brain MRI (required, any protocol; the gadolinium line on a non-contrast study and the hypertension reference are gone) and an optional medication review whose one output names tamsulosin and amlodipine. The literature step is gone; a DaTscan is waste (stored abnormal, left putamen worse); a stored battery matches his MoCA 27. The musts are the probable-PD diagnosis, levodopa titrated to 300 mg/day with lying and standing BP at each step, the agonist ICD/EDS warning, a driving assessment (his wife's concern, plus sleep attacks on dopaminergic drugs) and PT/OT/SLT. A red herring now uses his mother's undiagnosed late-life tremor.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan R1: `[NICE_NG71]` (levodopa, agonist, driving and therapy musts, DaTscan avoided action) is not yet in the PD criteria pack.
- Plan R4: an `olfactory_test` term would let an agent turn his self-reported smell loss into a validated supportive criterion; until then it stays non-supportive.

## Open questions for Andrea (judgment calls you could not settle)

- None specific to this case (plan Q1 to Q6 apply).

## Verification
- Checked against the committed rewrite (diff from b8be2153^, field by field), plans/PD.md section 4 entry and classes C1 to C23. No notes file exists for PD, so there is no note id to account for. Tools re-run 24 Oct 2026: perfect_agent ok, case_io check (no failure names the case), test_case_guards pass (leak, followup, banned strings), and a MockServer routing script (MRI or CT, DaTscan, MIBG, amyloid, FDG, PSG, battery, orthostatic BP, labs, ECG, drug check for levodopa and for rasagiline).
- Confirmed every row: literature removed; drug output names tamsulosin and amlodipine; gadolinium and "history of hypertension" lines gone; battery MoCA 27/30 matches the exam (TMT-B low-average for the visuospatial/executive point); DaTscan left putamen worse; ECG 69/min matches vitals; red herring path `family_history[1]` and text match the patient block.
- Verified the data the musts and evidence cite: driving concern (`social_history.driving`), constipation and self-reported smell loss (HPI paragraph 3), no falls, no dream enactment, manages finances. No supportive-criterion overcall.
- Found nothing to correct. No change made.

## Close-out (24 Oct 2026)

Decisions in `plans/PD-decisions.md`.

- Accepted codes are now G20.A1 (PD without dyskinesia, without mention of fluctuations; also PD NOS) and G20; G20.A2, G20.B1, G20.B2 (motor complications the case does not have) and G20.C ("Parkinsonism, unspecified", not PD) are no longer accepted. Labels unchanged.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
