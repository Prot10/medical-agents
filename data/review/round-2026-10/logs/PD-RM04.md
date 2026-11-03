# PD-RM04
Reviewer status: R1 none, R2 none (PD has no notes file; only the July 2026 tool review, `condition_tool_guidance.yaml` key `parkinsons`) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No physician note exists for PD. The case was corrected against plans/PD.md (classes C1 to C23, per-case entry PD-RM04) and the July 2026 tool review (MRI required; ECG, EEG, autonomic and tilt testing removed; labs, neuropsychology and genetics optional and targeted). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | major | `ground_truth.action_criteria[action-2-search-medical-literature]`, `followup_outputs[1]` | Required literature criterion with an exact `query` string; output with an empty summary and `[Postuma_2015]` and `[Marshall_2009]` embedded in `key_finding` text (C1, ruling 5). | FIXED: criterion and follow-up deleted, id removed from the stop rule; initial and fallback literature null. |
| A | major | `action-3-check-drug-interactions`, `followup_outputs[0]` | Drug criterion `required` with exact `drug` and `current_medications` strings; separate follow-up with em dashes and agonist alternatives (C2). | FIXED: `check_drug_interactions {}`, `optional` (no dopamine blocker on the list); one stored output `initial_tool_outputs.drug_interactions.general` (proposed carbidopa-levodopa; tamsulosin and amlodipine with orthostasis; MAO inhibitor contraindication; metformin, atorvastatin, acetaminophen no interaction); drug follow-up deleted, fallback null. Moved last in the criteria. |
| A | major | `action-1-analyze-brain-mri.alternatives` | Required `{"contrast": false, "protocol": "standard"}` (C5). | FIXED: `analyze_brain_mri {}`; canonical label and rationale; citations `[Postuma_2015]` and `[Schwarz_2014]` (the report has an SWI nigrosome finding). |
| B | major | `initial_tool_outputs.mri.findings` | The nigrosome-1 loss was filed under "Age-appropriate cortical atrophy" and again under "Normal midbrain morphology"; the pontine hot cross bun negative sat in the midbrain finding; "appropriate for age and vascular risk factors" referred to history (C12). | FIXED: one finding per structure (hemispheres with Fazekas 1 foci; basal ganglia normal, no putaminal rim; substantia nigra with bilateral nigrosome-1 loss; brainstem and cerebellum normal); observations and numbered impression rewritten without cross-modality text. `expected_evidence` restates the report. |
| C | major | `assessment.required_recommendations[1]`, `[3]`, `key_clinical_evidence[1]` | "Clinically established PD" with "levodopa responsiveness" and "hyposmia" as supportive criteria: he has never taken levodopa and his smell loss is self-reported (C6). | FIXED: canonical clinically probable PD must (rest tremor the one supportive criterion, no red flag); every levodopa-response claim deleted. |
| C | minor | `patient.neurological_exam.gait` | "Pull test: two steps backward before recovery (mild postural instability)": recovery within two steps is normal (MDS-UPDRS 3.12 score 0), and calling it postural instability adds an early-instability flag the case does not intend. | FIXED: "two steps backward with unaided recovery." |
| B | minor | `patient.neurological_exam.mental_status` | MoCA 24/30 "losing points on ... verbal fluency (2)": the MoCA letter-fluency item is worth one point, so the stated losses are impossible (found while auditing PD-RM05, same class). | FIXED: "attention/concentration (1), sentence repetition (1), verbal fluency (1), delayed recall (1), and abstraction (2)" (total 6, MoCA 24 unchanged). |
| B | major | `followup_outputs` PSG | One-sentence report "REM sleep without atonia confirming RBD, a strong prodromal synucleinopathy marker" with em dash (C10). | FIXED: full video-PSG (TST 338 min, efficiency 77%, REM latency 94 min, RSWA 36% of REM epochs against the SINBAR threshold, kicking and punching with shouting on video, AHI 3.4/h, SpO2 nadir 91%, PLMI 9/h) with the C10 impression; trigger `request_sleep_study`; criterion stays `optional` with a case-specific rationale citing `[Berg_2015]`. |
| E | minor | `followup_outputs` neuropsychological battery | Test names with em dashes; impression without a closing stop; generic `expected_evidence` "Characterize the cognitive profile" (C3). | FIXED: test names "Trail Making Test A, Time" etc.; impression in C10 form with the same domains (values and flags unchanged; flags agree with the stated ranges); `expected_evidence` restates the figures; trigger `request_neuropsych_testing`; criterion stays `optional`. |
| A | minor | `ground_truth.action_criteria` (missing), `followup_outputs` (missing) | Light-headedness on standing on tamsulosin and amlodipine with no lying and standing figures; the library would answer (C23). | FIXED: optional `orthostatic-bp` criterion after the MRI and a stored `ClinicalAssessmentReport` (supine 134/80 HR 72 equal to the vitals; 1 min 124/76 HR 79; 3 min 120/74 HR 80: fall 14/6, no orthostatic hypotension). |
| B | major | `followup_outputs` (missing) | No stored DaTscan: the library returns a normal scan, an MDS absolute exclusion that contradicts the label (C8). | FIXED: stored C8 PD report (right posterior putamen SBR 1.04, left 1.36, caudate spared; contralateral to the left-sided signs), trigger `request_datscan`; DaTscan added as `waste` in `avoided_actions` (clear clinical diagnosis, NICE NG71). No MRI-before-DaTscan constraint (no DaTscan criterion). |
| C | major | `ground_truth.assessment.required_recommendations` | Generic template musts ("Apply MDS 2015", "Review all current medications", "Initiate levodopa trial to confirm ... clinically established PD", "Refer to movement disorders"); no dose, no orthostatic or RBD management (C16). | FIXED: five musts: probable PD diagnosis; reframe the shoulder as parkinsonism and stop injections; canonical levodopa start (levodopa over an agonist at 73 with MoCA 24); lying and standing BP with tamsulosin and amlodipine review; RBD bedroom safety, melatonin over clonazepam. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | The orthopedic prohibition forbade "additional physical therapy", which remains appropriate in PD; antipsychotic prohibition non-canonical with em dashes. | FIXED: prohibition limited to further glenohumeral injections or capsular procedures; canonical D2-blocker prohibition; spine-surgery and anticholinergic prohibitions kept without em dashes. |
| C | minor | `ground_truth.differential` | Entries already low, but DLB, which the dream enactment and MoCA 24 raise, was missing; ET key features ignored the mother's tremor; MSA ignored the orthostatic symptom (ruling 7). | FIXED: DLB added `low` (no fluctuations, hallucinations or functional cognitive loss); ET, cervical, vascular, MSA and PSP key features rewritten with the excluding data; likelihoods unchanged. |
| D | major | `ground_truth.key_clinical_evidence` | Two "July 2026" engineering sentences (C4); "levodopa response, hyposmia" as supportive and "clinically established" (C6). | FIXED: six case-specific lines (parkinsonism, the shoulder presentation, MDS categorisation as probable, MRI, prodromal features with the smell test caveat, incidental spondylosis). |
| B | minor | `ground_truth.red_herrings` | `field_path` pointed at the whole history list. | FIXED: `past_medical_history[3]` (adhesive capsulitis) and `[2]` (spondylosis); interpretations restated against the exam. |
| B | minor | `ground_truth.avoided_actions` | One-phrase generic rationales; no guard on autonomic or tilt testing; ECG cited `[NICE_NG71]` for a claim NICE does not make (3.3). | FIXED: case-specific rationales; added `avoid-waste-datscan`, `avoid-waste-autonomic-testing`, `avoid-waste-tilt-table`; ECG cites `[Postuma_2015]`. |
| B | minor | `ground_truth.stop_rule` | Stop rule listed the literature and drug ids; `max_additional_actions` 0 (C20). | FIXED: MRI only; `max_additional_actions` 2. |
| B | minor | `fallback_tool_outputs.advanced_imaging`, `.echo`, `.ecg` | Amyloid fallback "does not resolve the current diagnostic question" (C11); echo without `echo_type` and "consistent with longstanding hypertension" (cross-modality); ECG rate 70 against HR 72 (C17). | FIXED: amyloid fallback null (library negative amyloid PET); echo `echo_type` TTE with concrete findings and impression; ECG "Sinus rhythm 72/min, normal axis and intervals, no ST change." |
| E | minor | `metadata.difficulty_rationale`, `.revision_reason`, `.last_revised` | Shared engineering text (C19). | FIXED: case-specific difficulty sentence (1 required criterion), revision reason per plan, 2026-10-24. |
| - | check | plan 3.6 | perfect_agent ok (MRI served by the initial output); case_io check: no failure names PD-RM04; test_case_guards pass (2/2); discriminator_defects empty. Routing: DaTscan, PSG, battery and orthostatic BP return the case reports; MIBG, amyloid and FDG return the library; `drug: levodopa`, `drug: rasagiline` and `{}` return the case output. | - |

## Changes, in one paragraph a physician can read before re-reviewing

This 73-year-old man has two years of left-sided parkinsonism (lost arm swing, then a "frozen shoulder" refractory to two injections and physiotherapy, a 4-5 Hz left rest tremor, decrement, cogwheel rigidity, micrographia), with self-reported smell loss, constipation, wife-reported dream enactment, light-headedness on standing and a MoCA of 24/30. The diagnosis is now clinically probable PD (MDS 2015): rest tremor is the only supportive criterion, since he has never taken levodopa and his smell loss was not tested; the old "clinically established, levodopa-responsive" claim is gone. The policy is a required brain MRI (any protocol), with optional lying and standing blood pressure, video-PSG, a neuropsychological battery and a medication review; the literature step is gone and DaTscan, autonomic and tilt testing are waste. The pull test of two steps is now recorded as normal recovery. The MRI is restructured one structure per finding (bilateral nigrosome-1 loss on SWI, Fazekas 1, normal midbrain, pons, putamina and cerebellum). New stored reports: orthostatic BP with no orthostatic hypotension (fall 14/6 mmHg), a full PSG with RSWA 36% and no sleep apnea, and an abnormal DaTscan (right putamen worse) so that the library's normal scan no longer contradicts the label. The musts are: diagnose probable PD; explain that the shoulder is parkinsonian rigidity and stop injections; start carbidopa-levodopa 25/100 half a tablet three times daily rising to 300 mg/day, preferred over an agonist at 73; lying and standing BP with review of tamsulosin and amlodipine; RBD bedroom safety with melatonin rather than clonazepam.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan R1: `[NICE_NG71]` (levodopa must, DaTscan waste rationale) is not yet in the PD criteria pack.
- Plan R4: a validated olfactory test (`olfactory_test`) is not orderable; his self-reported smell loss therefore cannot become a supportive criterion within the episode.

## Open questions for Andrea (judgment calls you could not settle)

- None specific to this case (plan Q1 to Q6 apply).

## Verification (adversarial verifier, 24 Oct 2026)
Read the log, the diff against master and the whole final case. Checked: MoCA item arithmetic (1+1+1+1+2 = 6, 24/30), pull test (2 steps with unaided recovery is MDS-UPDRS 3.12 score 0), orthostatic report against the vitals (supine 134/80 equals the vitals; fall 14/6, HR rise 8), DaTscan laterality (right putamen worse for left-sided signs), PSG and battery flags against their ranges, musts against prohibitions and avoided actions, differential against the final evidence, no claim of a levodopa response or validated smell test, no literature output, drug output names only his own medicines, fallbacks (amyloid null, echo TTE, ECG rate equal to the vitals). Every log claim matches the file.
Found: no error. Remaining em dashes in the HPI are original text, not new.
Changed: nothing.
Checks after the verification: `perfect_agent.py -v` ok, `case_io.py check` no failure names the case (the one suite failure is elsewhere), `test_case_guards` pass; MockServer routing re-checked by hand for the stored outputs named above.

## Condition audit

2026-10-24, PD condition auditor.

- `ground_truth.differential` "Adhesive capsulitis / musculoskeletal shoulder disease": M75.0 is a category; the case is the left shoulder, so M75.02.

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

- New optional criterion `olfactory-test` (`order_specialized_test {test_type: olfactory_test}`, `action_criteria[4]`, before the medication review) and its follow-up `request_olfactory_test_upsit` (`followup_outputs[4]`): UPSIT 21/40, severe microsmia, below the normal range for age and sex. Before, an olfactory order got the library's normosmia (35/40), which contradicts the smell loss in the history. Optional: the test can add an MDS supportive criterion but changes no management. No scoring change for an agent that does not order it.
- `ground_truth.assessment.required_recommendations[0]`: rewritten so the smell loss counts as a supportive criterion once a validated test confirms it (UPSIT 21/40), instead of saying it cannot be tested.
- `ground_truth.key_clinical_evidence[2]`: rewritten so the smell loss counts as a supportive criterion once a validated test confirms it (UPSIT 21/40), instead of saying it cannot be tested.
- `ground_truth.key_clinical_evidence[4]`: rewritten so the smell loss counts as a supportive criterion once a validated test confirms it (UPSIT 21/40), instead of saying it cannot be tested.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: levodopa_challenge}`: MDS-UPDRS III 31/132 OFF, 17/132 ON (45%) (fallback_tool_outputs.clinical_assessment). Why: rule 3: the stored exam documents parkinsonism; the library reports MDS-UPDRS III 3/132 with no parkinsonian signs.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}`: TUG 12.8 s, 10 m 1.01 m/s, Berg 50/56 (followup request_gait_and_balance_timed). Why: rule 3: the stored gait exam (arm swing, stride, turns, pull test) is abnormal; the library reports a normal gait, turns in 3 steps and Berg 56/56.
- `perform_clinical_assessment {assessment_type: cognitive_screen}`: MoCA 24/30 as in the exam (followup request_cognitive_screen). Why: rule 3: the stored exam records this MoCA and its items; the library reports MoCA 28/30 with other items.
- `order_specialized_test {test_type: speech_language_evaluation}`: hypophonia, articulation precise (65 dB SPL), no aphasia (fallback_tool_outputs.specialized_test). Why: rule 3: the stored exam records hypophonia; the library reports no motor speech disorder.
- `order_advanced_imaging {modality: MIBG_scan}`: early H/M 1.40, delayed 1.21, washout 41% (fallback_tool_outputs.advanced_imaging). Why: rule 1: cardiac sympathetic denervation is a supportive criterion of PD; the library reports normal uptake (H/M 2.4/2.6).
- `interpret_labs {panels: [HbA1c]}`: HbA1c 6.8% (treated diabetes) (fallback_tool_outputs.labs[HbA1c]). Why: rule 2: type 2 diabetes on treatment; the library reports 5.4%.

Checks: `perfect_agent.py` 30/30 PD pass; `test_case_guards.py -k PD-` and `pytest agent-platform/tests -k PD-` 300 passed (`test_grpo_rollout.py` not collected: training extra not installed); every criterion's served output unchanged (snapshot before/after); synonym guard 0 changes; no new report repeats a 60-character window of any `expected_evidence`; every listed term is answered without the library.
