# PD-RS01
Reviewer status: R1 none, R2 none (PD has no notes file; only the July 2026 tool review, `condition_tool_guidance.yaml` key `parkinsons`) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No physician note exists for PD. The case was corrected against plans/PD.md (classes C1 to C23, per-case entry PD-RS01) and the July 2026 tool review (MRI required; ECG, EEG, autonomic and tilt testing removed; labs, neuropsychology and genetics optional and targeted). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | major | `action-3-search-medical-literature`, `followup_outputs[0]`, `followup_outputs[2]` | Required literature criterion with an exact `query`; two literature outputs with unverifiable sources ("Journal of Clinical Movement Disorders 2021", a "Lancet Neurology 2019" non-motor paper) and a case-specific summary (C1, ruling 5). | FIXED: criterion and both follow-ups deleted, removed from the stop rule; initial and fallback literature null. |
| B | major | `action-2-check-drug-interactions.required_arguments`, drug follow-up | Copied from S01: `current_medications` listed acetaminophen (not taken) and omitted lithium and metformin; output called lithium a "minor interaction", advised separating iron or calcium (neither taken), em dashes (C2, C22). | FIXED: `check_drug_interactions {}`, `recommended`; one stored output `initial_tool_outputs.drug_interactions.general` from his own medicines: lithium C2 sentence (lisinopril raises the level), tamsulosin and lisinopril orthostatic sentences, dopaminergic drugs and mood elevation in bipolar disorder, NSAIDs and thiazides raising lithium; follow-up deleted, fallback null. |
| A | major | `action-1-analyze-brain-mri` | Required `{"contrast": false, "protocol": "standard"}` (C5); `expected_evidence` claimed a swallow-tail loss that the report never gives (C12). | FIXED: `analyze_brain_mri {}`; canonical label and rationale; `[Postuma_2015]` only; evidence restates the report. |
| B | major | `initial_tool_outputs.mri.impression`, `.additional_observations` | Impression "No ... white matter lesion" contradicts its own finding of scattered punctate T2/FLAIR foci; "no pathological enhancement" on a non-contrast study (C12). | FIXED: impression names the few punctate foci (Fazekas 1); enhancement wording removed. |
| C | major | `action-4-interpret-labs` | Labs `optional` with a three-panel argument and generic evidence; RPR padding; lab interpretation in "Abnormal values" form with "known DM2" cross-references (C3, C11). | FIXED: `recommended`, `interpret_labs {"panels": ["lithium_level"]}`, case-specific rationale (lisinopril raises lithium; lithium-induced hypothyroidism) and evidence (lithium 0.72, creatinine 1.1, TSH 2.14, free T4 1.2); RPR row deleted; interpretation and summary reduced to values and flags. Routing checked: the lithium order returns the case panel. |
| C | major | `followup_outputs` (missing), `ground_truth.action_criteria` | No stored DaTscan: the library would answer "normal", an MDS absolute exclusion (C8). | FIXED: optional `datscan` criterion (lithium is a live drug-related alternative) and a stored C8 report (left putamen 1.02, right 1.38, caudates 2.30 and 2.47; left deficit opposite the worse right side); soft MRI-before-DaTscan constraint. |
| C | major | `followup_outputs` PSG | "Abnormal values" impression with H/L flags, no RSWA percentage, em dashes (C10). | FIXED: full report keeping the stored figures (TST 342, efficiency 78%, REM latency 95, AHI 3.2, PLMI 8.4), RSWA 31% against the SINBAR threshold, SpO2 nadir 91%, video arm movements with vocalization; C10 impression; criterion stays `optional`, rationale `[Berg_2015]`; trigger `request_sleep_study`. |
| C | minor | `patient.neurological_exam.coordination` | "Mild terminal dysmetria on the right, likely secondary to tremor": a cerebellar sign is an MDS absolute exclusion and lithium causes cerebellar toxicity, so the exam line created an unintended exclusion the case never resolves. | FIXED: finger-to-nose accurate, tremor persisting during the movement, no dysmetria or intention tremor. |
| E | minor | `patient.neurological_exam.cranial_nerves` | "Mild bilateral facial symmetry preserved" (garbled). | FIXED: "Facial strength symmetric." |
| E | minor | every criterion `rationale`, `citations` | Rationale a copy of the label; bare duplicate keys (C3). | FIXED. |
| C | major | `ground_truth.assessment.required_recommendations` | Template musts; "classic for idiopathic PD"; agonist offered as equal first line in a man with bipolar disorder; no lithium management (C6, C16). | FIXED: six musts: C6 probable PD; do not attribute the syndrome to therapeutic lithium, keep it under psychiatry with level and renal monitoring; canonical levodopa start with lying and standing BP (tamsulosin); prefer levodopa to an agonist, with the ICD/EDS warning and mood monitoring with psychiatry; RBD bedroom safety (melatonin over clonazepam); physiotherapy and speech therapy. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Overlapping D2 prohibitions with an em dash. | FIXED: canonical D2 prohibition (relevant: bipolar disorder); new "do not stop lithium abruptly or without psychiatric input" (manic relapse); anticholinergic prohibition kept. |
| C | major | `ground_truth.differential` | ET `moderate` "sister with ET" (copied from S01; RS01 has a brother); no lithium entry (C13, C22). | FIXED: lithium-associated tremor and parkinsonism added `low`; ET `low` (brother, postural component); D2-blocker DIP, vascular, PSP `very_low`; MSA `low`; each with excluding data. |
| D | major | `ground_truth.key_clinical_evidence` | Two "July 2026" engineering sentences (C4); "clinically established PD" on one supportive criterion; "sister" and "baseline labs suffice" text from S01 (C6, C22). | FIXED: six case-specific lines (one supportive criterion, probable PD; prodromal markers; lithium level and thyroid; MRI; orthostatic figures). |
| B | major | `ground_truth.red_herrings` | "Sister with ET and 10 pack-year smoking": RS01 has a brother with ET and never smoked (C14, C22). | FIXED: lithium (`medications[0]`) and brother's ET (`family_history[2]`) with correct interpretations. |
| B | minor | `ground_truth.avoided_actions` | Generic rationales; no autonomic or tilt guard. | FIXED: case-specific rationales; `avoid-waste-autonomic-testing`, `avoid-waste-tilt-table` added. |
| B | minor | `ground_truth.sequence_constraints`, `.stop_rule` | "Labs before drug check" constraint with a reason that does not fit; stop rule listed literature and drug; `max_additional_actions` 0 (C20). | FIXED: one soft MRI-before-DaTscan constraint; stop rule MRI; `max_additional_actions` 2. |
| A | minor | `fallback_tool_outputs.echo` | No `echo_type`; vague text (C17). | FIXED: `echo_type` TTE, concrete normal finding. |
| E | minor | `metadata.difficulty_description`, `.difficulty_rationale`, `.revision_reason`, `.last_revised` | "Supportive non-motor features" (RBD and self-reported smell loss are not MDS supportive criteria); em dash; shared engineering text (C19). | FIXED. |
| - | check | plan 3.6 | perfect_agent ok (MRI and labs from the initial outputs, medication review from the initial drug output); case_io check: no failure names PD-RS01; test_case_guards 2 passed. Routing: DaTscan and PSG return the case reports; the lithium lab order returns the case panel; `drug: levodopa` and `drug: rasagiline` return the case output; the library battery (normal) fits MMSE 29/30; MIBG, amyloid, FDG and orthostatic BP return library normals, which fit (no orthostatic fall on exam). | - |

## Changes, in one paragraph a physician can read before re-reviewing

This 69-year-old man on lithium for bipolar disorder has an 18-month right-predominant parkinsonism with a 4-5 Hz pill-rolling rest tremor, decrement, rigidity, micrographia and hypophonia, plus 2 years of wife-witnessed dream enactment, constipation and self-reported smell loss. The case had been copied from S01 (a sister with ET, smoking, acetaminophen); its drug review, red herrings and differential are now rebuilt from his own data (lithium, lisinopril, tamsulosin, a brother with ET). The policy is MRI (required), the lithium level (recommended: lisinopril raises it) and a medication review (recommended), with optional DaTscan (now stored: asymmetric left putaminal deficit) and optional video-PSG (now a full report, RSWA 31%); the literature steps are gone. The MRI impression now names its own Fazekas 1 foci. The ambiguous "terminal dysmetria" in the exam, a cerebellar sign that would be an MDS absolute exclusion, is replaced by an accurate finger-to-nose with tremor. The diagnosis is clinically probable PD, not "established" (one supportive criterion). The musts add the lithium plan (do not blame the therapeutic level, monitor it, never stop lithium abruptly), levodopa in preference to an agonist in bipolar disorder, RBD bed safety and therapy referrals.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan R1: `[NICE_NG71]` (levodopa and agonist musts) is not yet in the PD criteria pack.
- Plan R5: the library MIBG default is normal; MIBG is not on this pathway, but a condition-aware default (reduced in PD) would be more coherent.

## Open questions for Andrea (judgment calls you could not settle)

- None specific to this case (plan Q1 to Q6 apply).

## Verification (adversarial verifier, 24 Oct 2026)
- Read the log, the diff and the whole final case. No PD notes file exists.
- Checked: medication list is RS01's own (lithium, lisinopril, metformin, atorvastatin, tamsulosin; no acetaminophen anywhere); drug output names only those drugs, lithium sentence canonical; lithium level 0.72 (1200 mg/day) with creatinine, TSH and free T4 normal in the stored panel, matching the lab criterion and the musts; brother (not sister) with ET and never smoker everywhere; dysmetria removed from the exam, no other cerebellar sign; DaTscan stored, left putamen deficit opposite the right-sided signs, optional, with the soft MRI-before-DaTscan constraint; PSG full report with RSWA 31%; orthostatic figures in the exam (138/82 to 134/80) consistent with differential and evidence; probable PD (one supportive criterion); MRI impression now names its Fazekas 1 foci; no swallow-tail claim.
- No error found that needs a change. Nothing edited.
- Checks re-run after verification: `perfect_agent.py -v` pass; `case_io.py check` schema OK, no failure names the case; `test_case_guards -k` pass; MockServer routing: DaTscan, MIBG and amyloid return their own modality (case or library), PSG and battery return the case report where stored, `check_drug_interactions` with `drug: levodopa` and `drug: rasagiline` return the case output, labs route to the stored panel where one exists; grep for established / gadolinium / "Abnormal values:" / Lewy / serotonin syndrome / Tier per / July 2026 / dashes: only allowed hits.

## Condition audit

2026-10-24, PD condition auditor.

- `fallback_tool_outputs.csf`: CSF glucose 62 mg/dL with ratio 0.6 did not fit the stored serum glucose of 118 mg/dL (true ratio 0.53). Glucose now 71 mg/dL (ratio 0.6), interpretation states the CSF glucose is in proportion to the raised serum glucose.

After the edits: `perfect_agent.py` 30/30 PD pass; every stored follow-up of the 30 cases is served for its own discriminator (MockServer probe); `case_io.py check` schema and synonym guard OK, the only suite failure is `test_guidance_claims` (expected); `test_case_guards.py -k PD-` 60 passed.

## Close-out (24 Oct 2026)

Decisions in `plans/PD-decisions.md`.

- Accepted codes are now G20.A1 (PD without dyskinesia, without mention of fluctuations; also PD NOS) and G20; G20.A2, G20.B1, G20.B2 (motor complications the case does not have) and G20.C ("Parkinsonism, unspecified", not PD) are no longer accepted. Labels unchanged.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Lab evidence (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited results its own order (the first alternative) no longer returned; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-4-interpret-labs]`.alternatives: was [lithium_level]; now [lithium_level, BMP, thyroid] | [lithium_level].
- Decision: serve: new first alternative (old order kept as an alternative). The label asks for the lithium level with renal and thyroid function; creatinine, TSH and free T4 were not returned by the level alone.
- Scoring: none (recommended criterion: coverage unchanged, not in the cost reference).

Checks: `perfect_agent.py` ok (the order returns every result its evidence cites); `case_io.py check` clean for this case.

## Batch-5 vocabulary (25 Oct 2026)

Commit c02f3050 added `cysticercosis_serology`, `IGRA` (interpret_labs), `olfactory_test` (order_specialized_test) and `levodopa_challenge` (perform_clinical_assessment); `HBV_DNA` (interpret_labs) was added the same day for this round. The requests are now wired into the case.

- New optional criterion `olfactory-test` (`order_specialized_test {test_type: olfactory_test}`, `action_criteria[4]`, before the medication review) and its follow-up `request_olfactory_test_upsit` (`followup_outputs[2]`): UPSIT 24/40, severe microsmia, below the normal range for age and sex. Before, an olfactory order got the library's normosmia (35/40), which contradicts the smell loss in the history. Optional: the test can add an MDS supportive criterion but changes no management. No scoring change for an agent that does not order it.
- `ground_truth.assessment.required_recommendations[0]`: rewritten so the smell loss counts as a supportive criterion once a validated test confirms it (UPSIT 24/40), instead of saying it cannot be tested.
- `ground_truth.key_clinical_evidence[1]`: rewritten so the smell loss counts as a supportive criterion once a validated test confirms it (UPSIT 24/40), instead of saying it cannot be tested.
