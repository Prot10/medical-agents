# PD-RS05
Reviewer status: R1 none, R2 none (PD has no notes file; only the July 2026 tool review, `condition_tool_guidance.yaml` key `parkinsons`) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No physician note exists for PD. The case was corrected against plans/PD.md (classes C1 to C20, per-case entry PD-RS05) and the July 2026 tool review (MRI required; ECG, EEG, autonomic and tilt testing removed; labs optional and targeted; genetics only for young onset or a significant family history). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.demographics.handedness`, `patient.history_present_illness` | Recorded as left-handed, but every writing complaint (calligraphy, whiteboard, micrographia "worst in the right hand") is in the right hand, the hand she writes with. | FIXED: handedness `right`; HPI "right-handed". |
| B | minor | `patient.neurological_exam.additional` | Smell loss "over the past year" against "approximately 18 months ago" in the HPI; "No anosmia formally tested" is malformed. | FIXED: "Olfaction not formally tested; she reports a decreased sense of smell first noticed about 18 months ago." |
| A | major | `action-3-search-medical-literature`, literature follow-up | Required literature criterion with an exact `query`; its expected evidence "support clinically established PD" (C1). | FIXED: criterion and follow-up deleted; initial and fallback literature null. |
| A | major | `action-2-check-drug-interactions`, drug follow-up | Required with exact `drug` and `current_medications` strings; output with em dashes, a "benign" rasagiline-topiramate interaction stated as fact, rasagiline and three agonists listed as alternatives, and advice to take levodopa 30-60 minutes before meals that contradicts the start-with-food must (C2). | FIXED: `check_drug_interactions {}`, `optional`; one stored `initial_tool_outputs.drug_interactions.general` naming only her medicines (topiramate cognitive effects without a levodopa interaction, omeprazole, cetirizine sedation), protein-distribution warning and her codeine intolerance; follow-up deleted, fallback null. Guard leak test passes. |
| A | major | `action-1-analyze-brain-mri` | Required `{"contrast": false, "protocol": "standard"}` (C5); "normal or equivocal swallow-tail" against a report that says preserved bilaterally; label equals rationale; bare key. | FIXED: `analyze_brain_mri {}`; canonical label and rationale; evidence restates the report (Evans 0.25, nigrosome-1 preserved); `[Schwarz_2014]` kept because the report gives an SWI finding. |
| C | minor | `action-4-interpret-labs`, `initial_tool_outputs.labs` | Generic criterion text; "Abnormal values" interpretation; summary "elevated; free T4 normal" with an em dash. | FIXED: optional, one-item alternatives `TSH` and `thyroid`, case rationale (her slowing is attributed to the TSH), evidence from the stored values; interpretation "Abnormal: TSH 5.8 mIU/L (H). Other results within reference ranges." Values unchanged: the PMH says the most recent TSH is 5.8, so the stored panel matches it. |
| C | major | `ground_truth.avoided_actions`, `followup_outputs` (missing) | No stored DaTscan: the library default (normal) is an MDS absolute exclusion and contradicts the label (C8). | FIXED: DaTscan `waste` with a stored C8 report (left putamen SBR 1.06, right 1.35; left deficit opposite the right-sided signs; matches the seed note). |
| C | major | `ground_truth.assessment.required_recommendations` | Six template musts; "anosmia" (self-reported) and constipation offered as "supportive evidence"; constipation "14 months" against "past year" in the HPI; vague "carbidopa-levodopa or a dopamine agonist" (C6, C15, C16). | FIXED: five musts: C6 probable PD; subclinical hypothyroidism explained and left to endocrine monitoring; canonical levodopa start; agonist caution (56 years); physiotherapy for the near-falls on turning, occupational therapy for fine hand tasks, speech therapy for hypophonia. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Three overlapping prohibitions with em dashes; "no anticholinergic over age 50" is not a guideline rule (in a 56-year-old with intact cognition, MoCA 28/30, an anticholinergic for tremor is a recognised if second-line option). | FIXED: canonical D2 prohibition only; anticholinergic prohibition removed. |
| B | minor | `ground_truth.differential` | No ICD codes for four entries; DIP `low` while the history excludes exposure; key features not tied to the case data. | FIXED: ICD codes (E03.9, G21.19, G21.4, G23.1); ET `low` (no family ET), hypothyroid slowing `low` "coexists", DIP, vascular, MSA, PSP `very_low` with the excluding findings. |
| D | major | `ground_truth.key_clinical_evidence` | Two "July 2026" engineering lines (C4); "clinically established PD" with anosmia and constipation as support (C6). | FIXED: five case-specific lines; probable PD with one supportive criterion; smell loss stated as not supportive. |
| B | minor | `ground_truth.red_herrings[0]` | Data point with an em dash; pointed only at the optional lab, while the agent sees the TSH in the PMH and HPI. | FIXED: `field_path` `patient.clinical_history.past_medical_history[0]`, location lists PMH, HPI and labs; text rewritten. |
| B | minor | `ground_truth.avoided_actions` | Generic rationales; no autonomic or tilt guard. | FIXED: case-specific rationales; DaTscan, autonomic and tilt `waste` added. |
| B | minor | `ground_truth.sequence_constraints`, `.stop_rule` | "Drug check before labs" constraint with an unfitting reason; stop rule with literature and drug ids; 0 extra actions (C20). | FIXED: no constraint (DaTscan is waste); stop rule MRI only; `max_additional_actions` 2. |
| A | minor | `fallback_tool_outputs.echo`, `.ecg` | Echo without `echo_type`; ECG rate 65 against a resting HR of 66 (C17). | FIXED: TTE with concrete text (EF 63%); ECG "Sinus rhythm 66/min, normal axis and intervals, no ST change." |
| E | minor | `metadata.difficulty_description` (missing), `.difficulty_rationale`, `.revision_reason`, `.last_revised` | Shared engineering text (C19). | FIXED. `difficulty` stays `straightforward`. |
| C | - | genetics | Father with PD at 74, her onset at 55: not young onset and one late-onset relative; genetics not indicated (plan). | No criterion (unchanged). |
| - | check | plan 3.6 | perfect_agent ok (MRI served by `initial_tool_outputs.mri`, verified with MockServer; `-v` prints "?" only because of the dump comparison); case_io check: no failure names PD-RS05; test_case_guards 2 passed; discriminator_defects empty. Routing: DaTscan returns the case report; MIBG and amyloid the library; labs `TSH`/`thyroid` the stored panel; `drug: levodopa` and `drug: rasagiline` the case output; library PSG (normal) fits a history without dream enactment; library battery (normal) fits MoCA 28/30. | - |

## Changes, in one paragraph a physician can read before re-reviewing

A 56-year-old woman with 14 months of right-sided parkinsonism (pill-rolling rest tremor with re-emergence, decrement, cogwheel rigidity, micrographia, hypomimia, hypophonia, two near-falls on turning, MoCA 28/30) and subclinical hypothyroidism to which her slowing had been attributed. She is now right-handed, as her right-hand writing complaints require, and the onset of her self-reported smell loss reads the same in history and exam. The policy is brain MRI only (required); thyroid labs and a medication review are optional; the literature step is gone; DaTscan, EEG, CSF, ECG, echo, Holter, autonomic and tilt testing are waste (a stored abnormal DaTscan, left putamen, answers anyone who orders it). The musts now diagnose clinically probable PD (rest tremor is the only supportive criterion; self-reported smell loss and constipation are not), explain that the TSH of 5.8 with normal free T4 does not cause the parkinsonism, start carbidopa-levodopa at the canonical dose with food, warn about impulse control disorders if an agonist is used, and refer to physiotherapy, occupational and speech therapy. The generic anticholinergic prohibition ("age over 50") was removed as not guideline-based for this cognitively intact 56-year-old.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan R1: `[NICE_NG71]` (levodopa and agonist musts, DaTscan and ECG waste) is not yet in the PD criteria pack.
- Plan R4: a validated smell test (`olfactory_test`) is not orderable, so her smell loss can only stay self-reported.
- Plan R5: library MIBG default normal (not on this pathway; in PD it would usually be reduced).

## Open questions for Andrea (judgment calls you could not settle)

- None specific to this case. Plan Q4 applies (DaTscan waste in a clinically clear case).

## Verification (adversarial verifier, 24 Oct 2026)
- Read the log, the uncommitted diff and the whole final case. No PD notes file exists.
- Checked: handedness correction to right is supported (all writing complaints and micrographia in the right hand); smell-loss onset (18 months) matches HPI and exam; TSH 5.8 with free T4 1.1 identical in PMH, HPI, stored labs, criterion, must and red herring; lab panel names `TSH` and `thyroid` in the vocabulary; red herring points to `past_medical_history[0]` rather than the optional labs (plan asked for the thyroid panel; the PMH entry carries the same value and is what the agent sees, so the deviation is sound); drug output names only her medicines and the codeine intolerance; DaTscan waste with a left-putamen report opposite the right-sided signs; no genetics criterion (father onset 74, hers 55); removal of the anticholinergic prohibition is defensible at 56 with MoCA 28; probable PD.
- No error found that needs a change. Nothing edited.
- Checks re-run after verification: `perfect_agent.py -v` pass; `case_io.py check` schema OK, no failure names the case; `test_case_guards -k` pass; MockServer routing: DaTscan, MIBG and amyloid return their own modality (case or library), PSG and battery return the case report where stored, `check_drug_interactions` with `drug: levodopa` and `drug: rasagiline` return the case output, labs route to the stored panel where one exists; grep for established / gadolinium / "Abnormal values:" / Lewy / serotonin syndrome / Tier per / July 2026 / dashes: only allowed hits.

## Close-out (24 Oct 2026)

Decisions in `plans/PD-decisions.md`.

- Accepted codes are now G20.A1 (PD without dyskinesia, without mention of fluctuations; also PD NOS) and G20; G20.A2, G20.B1, G20.B2 (motor complications the case does not have) and G20.C ("Parkinsonism, unspecified", not PD) are no longer accepted. Labels unchanged.
