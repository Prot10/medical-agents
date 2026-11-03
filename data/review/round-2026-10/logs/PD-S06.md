# PD-S06
Reviewer status: R1 none, R2 none (PD has no notes file; only the July 2026 tool review, `condition_tool_guidance.yaml` key `parkinsons`) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No physician note exists for PD. The case was corrected against plans/PD.md (classes C1 to C23, per-case entry PD-S06) and the July 2026 tool review (MRI required, CT as the alternative here; ECG, EEG, autonomic and tilt testing removed; labs, neuropsychology and genetics optional and targeted). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | major | `ground_truth.action_criteria[action-2-search-medical-literature]`, `followup_outputs[1]` | Required literature criterion with an exact `query` string; output cited a "Tolosa, Wenning, Poewe, Lancet Neurol 2006" paper under a title that does not match it (C1, ruling 5). | FIXED: criterion and follow-up deleted, removed from the stop rule; initial and fallback literature null. |
| A | major | `action-1-check-drug-interactions`, `followup_outputs[0]` | Required drug check with exact `drug` and `current_medications` strings, listed first; output claimed calcium-rich meals compete with levodopa absorption (it is iron that chelates levodopa) and carried em dashes (C2). | FIXED: `check_drug_interactions {}`, tier `optional`, moved after the imaging; one stored output `initial_tool_outputs.drug_interactions.general` (lisinopril orthostatic sentence; non-selective MAOI contraindication; alendronate, calcium, vitamin D3, atorvastatin no relevant interaction; iron not calcium; nausea, protein, sleep attacks, ICD warnings); follow-up deleted, fallback null. |
| A | major | `action-3-order-ct-scan` | `{"contrast": false}` argument too narrow (C5); listed third; bare duplicate key; rationale copied from label (C3). | FIXED: `order_ct_scan {}`, placed first; plan S06 rationale; `[Postuma_2015]`; expected_evidence restates the report. Stays `required` with its `panel_required_exemptions.analyze_brain_mri`. |
| D | major | `initial_tool_outputs.ct.additional_observations`, `.impression` | Report contained history ("MRI was not completed because severe claustrophobia persisted...") and an impression about "the parkinsonian syndrome" with a meta sentence on its own sensitivity. | FIXED: history sentence deleted; within-modality limitation line kept; impression "No acute intracranial abnormality. Mild age-appropriate volume loss without disproportionate ventriculomegaly. No basal ganglia infarct, mass or hydrocephalus." |
| B | minor | `fallback_tool_outputs.mri` | An agent ordering the MRI the patient declined received the library "Normal MRI of the brain". | FIXED: case fallback "MRI not performed: no diagnostic images acquired." (examination abandoned, claustrophobia, sedation declined), following the SYNC-CARD "not performed" precedent. |
| D | major | `followup_outputs` DaTscan | Interpretive report ("period or dot pattern"), em dash impression, `quantitative_data` null (C8). | FIXED: C8 binary report: right posterior putamen SBR 1.02, left 1.37 (normal >1.50), caudates 2.26 and 2.42, contralateral to the left-sided signs; trigger kept. |
| C | minor | `action-4-order-advanced-imaging` | Optional DaTscan with generic label, rationale and shared expected_evidence (C3, C8). | FIXED: stays `optional`; case-specific label, rationale (mother's tremor and postural tremor raise ET; PD clinically likely) [NICE_NG71], expected_evidence restating the figures; soft CT-before-DaTscan constraint added (the canonical MRI-before-DaTscan constraint, with CT as this case's structural study). |
| D | major | `ground_truth.key_clinical_evidence` | Two "July 2026" engineering sentences (C4); "DaTscan laterality is mandatory" built on an optional study (C8 rule 6); self-reported hyposmia counted as a prodromal support; em dashes. | FIXED: six case-specific lines; hyposmia called self-reported. |
| C | major | `ground_truth.assessment.required_recommendations` | Generic musts; "hypomimia and asymmetry are supportive features" (they are not, F1); "hyposmia support a synucleinopathy prodrome" from a self-report; em dashes (C6, C16). | FIXED: four musts: probable-PD diagnostic must, canonical levodopa start, lying and standing BP during titration (lisinopril), PT (with fall prevention given osteoporosis and a previous fall-related wrist fracture), OT and SLT. No agonist must (age 71). |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Generic prohibitions with em dashes. | FIXED: canonical D2-blocker prohibition; anticholinergic prohibition at 71. |
| C | major | `ground_truth.differential[Essential tremor]` | ET `high` (C13); MSA and PSP features cited an MRI that does not exist ("no pontine atrophy on MRI", "midbrain atrophy"). | FIXED: ET `low` with the excluding exam; MSA and PSP rewritten on clinical data only. |
| B | minor | `ground_truth.red_herrings[0].correct_interpretation` | Em dashes; counted self-reported hyposmia as incompatible with ET. | FIXED: rewritten on the motor findings. |
| C | minor | `fallback_tool_outputs.advanced_imaging`, `avoided_actions` | Amyloid PET fallback that "does not resolve the current diagnostic question" (C11); generic avoided-action rationales; no autonomic or tilt guard. | FIXED: amyloid fallback null (library negative); case-specific rationales; autonomic and tilt waste added. |
| A | minor | `fallback_tool_outputs.ecg`, `.echo` | ECG rate 65 against HR 67; echo without `echo_type` (C17). | FIXED: ECG "Sinus rhythm 67/min, normal axis and intervals, no ST change."; echo `TTE`, EF 60%. |
| E | minor | `patient.history_present_illness`, `.clinical_history.family_history[0]`, `.social_history.alcohol`, `neurological_exam.gait`, `.motor` | Em and en dashes in patient text. | FIXED: replaced by commas, semicolons or hyphens; wording otherwise unchanged. |
| B | minor | `ground_truth.stop_rule` | Drug and literature ids; `max_additional_actions` 0 (C20). | FIXED: CT only; 2. |
| E | minor | `metadata.estimated_complexity`, `.difficulty_rationale`, `.revision_reason`, `.last_revised` | Em dash; shared engineering metadata (C19). | FIXED. |
| - | check | plan 3.6 | perfect_agent ok (CT from the initial output); case_io check: no failure names PD-S06; test_case_guards pass; discriminator_defects empty. Routing: DaTscan returns the case report; MRI returns the case "not performed" fallback; PSG and battery library normals (no dream enactment, MoCA 28/30); amyloid, MIBG, FDG library; `drug: levodopa` and `drug: rasagiline` return the case output. | - |

## Changes, in one paragraph a physician can read before re-reviewing

This 71-year-old woman has a 2.5-year left-sided tremor-onset parkinsonism (pill-rolling rest tremor that re-emerges at rest, decrement, cogwheel rigidity, micrographia, hypophonia), self-reported smell loss, constipation and a mother with undiagnosed "shaky hands"; she declined MRI for severe claustrophobia. She is now clinically probable PD (rest tremor the only supportive criterion; hypomimia and asymmetry are not supportive criteria). The policy is a non-contrast head CT first (required, any arguments; the report no longer narrates the MRI history), an optional DaTscan for the familial tremor question (binary report, right putamen 1.02, after the CT) and an optional medication review naming lisinopril; the literature step is gone, and the false calcium-levodopa interaction is removed. An MRI order now returns "not performed" instead of a library normal MRI. The musts are the probable-PD diagnosis, levodopa titrated to 300 mg/day, lying and standing BP during titration, and PT with fall prevention (osteoporosis, previous fall fracture), OT and SLT. ET is now low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan R1: `[NICE_NG71]` (DaTscan criterion, levodopa and therapy musts) is not yet in the PD criteria pack.

## Open questions for Andrea (judgment calls you could not settle)

- None specific to this case (plan Q1 to Q6 apply). The "MRI not performed" case fallback is a small addition outside the plan, made so that the agent is not told a declined MRI was normal.

## Verification
- Checked against the committed rewrite (diff from b8be2153^, field by field), plans/PD.md section 4 entry and classes C1 to C23. No notes file exists for PD, so there is no note id to account for. Tools re-run 24 Oct 2026: perfect_agent ok, case_io check (no failure names the case), test_case_guards pass (leak, followup, banned strings), and a MockServer routing script (MRI or CT, DaTscan, MIBG, amyloid, FDG, PSG, battery, orthostatic BP, labs, ECG, drug check for levodopa and for rasagiline).
- Confirmed every row: CT `{}` first and required with its `panel_required_exemptions.analyze_brain_mri`; the CT report no longer narrates history; MRI fallback "not performed" is served for `analyze_brain_mri` and agrees with the HPI; DaTscan optional, right putamen worse (contralateral to the left-sided signs), soft CT-before-DaTscan constraint; amyloid fallback null (library negative, and amyloid is waste with a MoCA 28/30 rationale); ET `low`; dash changes in the patient block alter no wording.
- Found and fixed three small errors:
  - `initial_tool_outputs.drug_interactions.general.warnings[1]` read "Iron salts (not calcium) chelate levodopa": the parenthesis answered the deleted calcium claim and is not report voice. Now "Iron salts chelate levodopa and reduce its absorption; give iron at least 2 hours apart from levodopa if it is ever added."
  - `ground_truth.avoided_actions[avoid-waste-4-order-cardiac-monitoring].rationale` said "No syncope, falls or palpitations", but PMH records a fall with wrist fracture 12 years ago (cited by the physiotherapy must). Now "No syncope or palpitations, and no fall since the remote wrist fracture 12 years ago: rhythm monitoring is not indicated".
  - `ground_truth.differential[Progressive supranuclear palsy].key_features` "no falls" became "no falls since onset" for the same reason.

## Condition audit

2026-10-24, PD condition auditor.

- `followup_outputs[0].trigger_action`: `request_optional_datscan_for_live_degenerative_differential` carried a tier word; renamed `request_datscan`. Routing by `modality` `DaTscan`, unchanged.

After the edits: `perfect_agent.py` 30/30 PD pass; every stored follow-up of the 30 cases is served for its own discriminator (MockServer probe); `case_io.py check` schema and synonym guard OK, the only suite failure is `test_guidance_claims` (expected); `test_case_guards.py -k PD-` 60 passed.

## Close-out (24 Oct 2026)

Decisions in `plans/PD-decisions.md`.

- Accepted codes are now G20.A1 (PD without dyskinesia, without mention of fluctuations; also PD NOS) and G20; G20.A2, G20.B1, G20.B2 (motor complications the case does not have) and G20.C ("Parkinsonism, unspecified", not PD) are no longer accepted. Labels unchanged.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Batch-5 vocabulary (25 Oct 2026)

Commit c02f3050 added `cysticercosis_serology`, `IGRA` (interpret_labs), `olfactory_test` (order_specialized_test) and `levodopa_challenge` (perform_clinical_assessment); `HBV_DNA` (interpret_labs) was added the same day for this round. The requests are now wired into the case.

- New optional criterion `olfactory-test` (`order_specialized_test {test_type: olfactory_test}`, `action_criteria[2]`, before the medication review) and its follow-up `request_olfactory_test_upsit` (`followup_outputs[1]`): UPSIT 17/40, in the anosmic range, below the normal range for age and sex. Before, an olfactory order got the library's normosmia (35/40), which contradicts the smell loss in the history. Optional: the test can add an MDS supportive criterion but changes no management. No scoring change for an agent that does not order it.
- `ground_truth.assessment.required_recommendations[0]`: rewritten so the smell loss counts as a supportive criterion once a validated test confirms it (UPSIT 17/40), instead of saying it cannot be tested.
- `ground_truth.key_clinical_evidence[1]`: rewritten so the smell loss counts as a supportive criterion once a validated test confirms it (UPSIT 17/40), instead of saying it cannot be tested.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: levodopa_challenge}`: MDS-UPDRS III 24/132 OFF, 12/132 ON (50%) (fallback_tool_outputs.clinical_assessment). Why: rule 3: the stored exam documents parkinsonism; the library reports MDS-UPDRS III 3/132 with no parkinsonian signs.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}`: TUG 11.3 s, 10 m 1.11 m/s, Berg 52/56 (followup request_gait_and_balance_timed). Why: rule 3: the stored gait exam (arm swing, stride, turns, pull test) is abnormal; the library reports a normal gait, turns in 3 steps and Berg 56/56.
- `perform_clinical_assessment {assessment_type: cognitive_screen}`: MoCA 28/30 as in the exam (followup request_cognitive_screen). Why: rule 3: the stored exam records this MoCA and its items; the library reports MoCA 28/30 with other items.
- `order_specialized_test {test_type: speech_language_evaluation}`: hypophonia, articulation precise (65 dB SPL), no aphasia (fallback_tool_outputs.specialized_test). Why: rule 3: the stored exam records hypophonia; the library reports no motor speech disorder.
- `order_advanced_imaging {modality: MIBG_scan}`: early H/M 1.52, delayed 1.39, washout 34% (fallback_tool_outputs.advanced_imaging). Why: rule 1: cardiac sympathetic denervation is a supportive criterion of PD; the library reports normal uptake (H/M 2.4/2.6).

Checks: `perfect_agent.py` 30/30 PD pass; `test_case_guards.py -k PD-` and `pytest agent-platform/tests -k PD-` 300 passed (`test_grpo_rollout.py` not collected: training extra not installed); every criterion's served output unchanged (snapshot before/after); synonym guard 0 changes; no new report repeats a 60-character window of any `expected_evidence`; every listed term is answered without the library.
