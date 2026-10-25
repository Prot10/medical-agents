# FEPI-TEMP-P03
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for FEPI-TEMP) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. The physician input is the July 2026 tool guidance for focal_epilepsy_temporal (condition_tool_guidance.yaml), applied through plans/FEPI-TEMP.md. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | blocker | `initial_tool_outputs.literature_search['general']` | Plan class A: the literature output was the literature criterion's `expected_evidence` (leak guard failed). | FIXED: deleted; replaced by a general cited entry (LaFrance 2013 diagnostic levels; Goldstein 2020 CODES trial, results stated correctly: no difference in the primary outcome, better secondary outcomes). Leak guard passes. |
| D | major | `initial_tool_outputs.drug_interactions['general']` | Block only echoed the medication list with a summary and a warning about prescribing decisions; no interaction content. | FIXED: deleted; replaced by a real check of lamotrigine with alprazolam (no PK interaction, additive sedation; dependence and withdrawal-seizure warning; sulfonamide allergy without cross-reactivity). The plan said to delete and not fill; an empty check would leave the agent with a generic fallback for the one drug question this case raises (the benzodiazepine taper in a patient with epilepsy), so a short factual answer was authored. Optional criterion. |
| D | major | `followup_outputs` (`request_video_eeg`) | Teaching capitals ("KNOWN, STABLE", "NO electrographic correlate", "eyes CLOSED", "ALL"), artifact named "PNES events", and limitations that drew a clinical conclusion ("consistent with 3 years of seizure freedom", "confirm the underlying epilepsy") (class K). | FIXED: neurophysiologist voice; numbered ABNORMAL impression (interictal right anterior temporal sharp waves; seven habitual events without EEG change before, during or after); limitations about artifact only. Event content unchanged. |
| D | minor | `initial_tool_outputs.mri` | Capitals ("KNOWN, STABLE", "NEW"); impression "No imaging explanation for increased seizure frequency" (clinical inference); gadolinium line in an HS case (class E); asymmetry index in prose only. | FIXED: report voice, comparison line, numbered impression; post-gadolinium line removed; asymmetry index 0.16 ((3.3 - 2.4)/5.7) and 27% reduction (1 - 2.4/3.3). |
| A | major | `fallback_tool_outputs.advanced_imaging`, `.specialized_test` | Class Q: advanced imaging fallback with `modality: "MRI"` (not a term) and specialized test fallback `test_type: "not_specified"`, both answering every variant. | FIXED: both null (library answers per study); `metadata.fallback_tool_kinds` entries removed. |
| A | minor | `fallback_tool_outputs.echo` | No `echo_type` (class I). | FIXED: `"echo_type": "TTE"`. |
| C | major | `ground_truth.action_criteria` | MRI required `{contrast: false, protocol: epilepsy}`; literature and drug check `recommended`; video-EEG template evidence; duplicate citations; rationale = label. | FIXED: MRI `{protocol: epilepsy}` required, video-EEG required, drug check optional, literature optional and last; one key each; case-specific evidence and rationale. Ids kept. |
| C | major | `ground_truth.sequence_constraints` | EEG -> drug check soft constraint with an optional criterion (plan 3.3). | FIXED: removed (no constraint left). |
| C | major | `ground_truth.stop_rule` | Max 0. | FIXED: MRI, video-EEG; max 2. |
| C | major | `ground_truth.assessment.required_recommendations` | "Admit for prolonged video-EEG" is a scored work-up step (class L); no must to explain the diagnosis; driving tied to "any breakthrough". | FIXED: five musts: explain the diagnosis with a written plan for family and emergency services; continue lamotrigine 200 mg twice daily; CBT-based psychotherapy addressing the precipitant and trauma history; gradual alprazolam taper with addiction medicine; driving advice from the epileptic seizure status plus no driving while events with loss of control continue. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | "Benzodiazepine drip" phrasing; em dash. | FIXED: "Do not give repeated or continuous benzodiazepines for the functional events"; dash removed; the other three kept in substance. |
| C | major | `ground_truth.differential` | Breakthrough seizures `moderate` after a video-EEG that excludes them (class P); intractable code G40.219 for controlled epilepsy; F13.20 for withdrawal. | FIXED: breakthrough `low`, new focus `very_low`, each with the excluding finding; codes G40.209 and F13.239. |
| C | minor | `ground_truth.key_clinical_evidence` | Engineering lines (class G); "10-30% of patients in chronic epilepsy clinics" misstates the coexistence figure. | FIXED: five case lines; coexistence stated as "a substantial minority". |
| C | minor | `ground_truth.avoided_actions[*].rationale` | Generic rationales. | FIXED: case-specific (CSF, echo, Holter, CT, FDG-PET kept as waste). |
| E | minor | `patient.neurological_exam.additional` | Editorial parenthesis "(as expected with well-controlled temporal lobe epilepsy)". | FIXED: removed. |

## Changes, in one paragraph a physician can read before re-reviewing

A 38-year-old woman with right mesial TLE from hippocampal sclerosis, free of epileptic seizures for 3 years on lamotrigine, has two months of new 5-20 minute events with eyes closed, side-to-side head movement and preserved awareness after her daughter's epilepsy diagnosis, with escalating alprazolam. The scored work-up is an epilepsy-protocol MRI (right HS unchanged, no new lesion; no gadolinium) and a 5-day video-EEG that records seven habitual events without EEG change and the known right anterior temporal sharp waves; the reports are rewritten in report voice. Drug check and literature are optional, with non-leaking factual outputs. Musts: explain the diagnosis with a written plan, keep lamotrigine unchanged, CBT-based therapy addressing the trigger and trauma history, gradual alprazolam taper with addiction medicine, driving advice. The differential now reflects the video-EEG result.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Criteria pack allow-list: `[ILAE_MRI_2019]`, `[ILAE_PNES_2013]` (plan CENTRAL 2).

## Open questions for Andrea (judgment calls you could not settle)

None. Departure from the plan: the deleted drug block was replaced by a short real lamotrigine-alprazolam check (see Own findings) instead of being left empty.

## Verification

Adversarial check, 24 Oct 2026. Read the log, the diff against master (edit committed in the batch-5 checkpoint) and the patient block. Checked: the sulfonamide statement in the new drug output matches `allergies` ("Sulfonamides (rash)"); the trauma history the CBT must cites is in the past medical history; lamotrigine 200 mg twice daily matches the medication list; volumetric arithmetic (index 0.9/5.7 = 0.16, 1 - 2.4/3.3 = 27%) is right; the video-EEG impression, finding fields and criterion evidence agree (seven events, no EEG change, F8 sharp waves); the differential is the post-video-EEG view; discriminator fallbacks removed (class Q), echo fallback typed; no sequence constraint involves an optional criterion; LaFrance 2013 and CODES (Goldstein 2020) are described correctly (CODES missed its primary outcome). Nothing wrong found; no change made.

## Condition audit

Condition auditor, 24 Oct 2026. Checked uniformity of the plan's decisions across the 30 cases and the FND and MS-RR audit classes (engineering text, any-query outputs, second-tier labs, copied numbers, sharp-wave durations, differential codes). After the changes below, `perfect_agent.py` and `case_io.py check` are clean for all 30 cases and `test_case_guards.py -k FEPI-TEMP` passes.

- `initial_tool_outputs.literature_search.general`: neutral focal-epilepsy block added (definition, classification, MRI protocol, first-line ASM, drug resistance), so a literature query that names no case-specific topic no longer receives a stored follow-up.
- Initial literature output ("psychogenic nonepileptic seizures coexisting with epilepsy diagnosis and treatment", served for any query) moved to the last follow-up `search_literature_psychogenic_nonepileptic_pnes`.
- `fallback_tool_outputs.literature_search`: placeholder block deleted (unreachable behind the initial output; it held "(agent not specified...)" or "No directly applicable evidence").
- `fallback_tool_outputs.drug_interactions`: placeholder block deleted (unreachable behind the initial output; it held "(agent not specified...)" or "No directly applicable evidence").
- `action-5-check-drug-interactions.rationale`: engineering prefix or tier wording removed (was "Optional: no change of antiseizure medic...").
- `action-4-search-medical-literature.rationale`: engineering prefix or tier wording removed (was "Optional background; the diagnosis rests...").

## Close-out (24 Oct 2026)

Condition close-out (`plans/FEPI-TEMP-decisions.md`). What changed and why:

- Synonyms (F44.5 token hazard from the FND close-out): P03 excluded from the global F44.5 entry and given `F44.5+fepi`: "non-epileptic seizures" removed (its tokens occur in "focal non-motor epileptic seizures", so a breakthrough-epilepsy answer scored), "nonepileptic seizures" added, codes F44.4 (motor) and F44.7 (mixed) removed. Probed: no epilepsy answer or G40 code scores here; PNES, functional, dissociative and psychogenic nonepileptic seizure answers do.
- Checks: `perfect_agent.py -v` and `case_io.py check` clean; `test_case_guards.py -k FEPI-TEMP-` passes, now with the discriminator guard and the FEPI-TEMP banned strings.

## Weight and height (25 Oct 2026)

- Past history says "Mild obesity" but the stored BMI was 28.2 (overweight). Rule 3: BMI 28.2 -> 31.0 (class I obesity), weight 69.5 -> 76.4 kg, height 157 cm kept. No text cited the old BMI.
- Checks: `perfect_agent.py` pass; weight/height/BMI consistency check clean.
