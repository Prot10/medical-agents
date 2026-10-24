# FEPI-TEMP-M01
Reviewer status: R1 none, R2 none (no notes file for FEPI-TEMP) | Approved before this round: no

## Reviewer notes
No reviewer notes for this case. The physician input for FEPI-TEMP is the July 2026 tool guidance (plan 1.3), applied through the plan.

| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | - |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | blocker | `initial_tool_outputs.mri` (plan F, E) | The only MRI was an equivocal 1.5T study ("does not meet definitive criteria for mesial temporal sclerosis", right hippocampus 12th percentile, AI 0.08) while the label is right mesial temporal sclerosis and the criterion orders an epilepsy-protocol MRI; gadolinium lines in a non-lesional HS study. | FIXED: rewritten as the dedicated 3T epilepsy-protocol MRI (technique line, no contrast) with definite right HS (volume loss 2.5 vs 3.5 cm3, 29% smaller, AI 0.17 by (L-R)/(L+R), T2/FLAIR hyperintensity, loss of internal architecture, mild right temporal horn enlargement); the two right frontal white matter foci kept as nonspecific and "unchanged from the outside 1.5T study"; gadolinium lines deleted. |
| B | major | `patient.history_present_illness` (plan F) | "No prior neuroimaging" while the case is built on a missed standard MRI. | FIXED: an outside standard 1.5T MRI three months ago, read as two nonspecific right frontal white matter foci and otherwise normal, is now in the HPI. |
| D | major | `followup_outputs[0]` FDG-PET (plan J) | FDG-PET follow-up that no criterion orders, in a first diagnosis with concordant MRI and EEG. | FIXED: removed from the pathway and moved to `fallback_tool_outputs.advanced_imaging` (modality `FDG_PET`, uptake ratio 0.87 written as a ratio, not an "asymmetry index"; `metadata.fallback_tool_kinds.advanced_imaging: case`); new avoided action `avoid-waste-5-order-advanced-imaging-fdg-pet` (waste, `[Willmann_2007]`, canonical rationale). Routing checked: an FDG_PET order receives the fallback. |
| B | major | `followup_outputs[*]` sleep-deprived EEG (plan K) | Limitations copied from a video study ("Only one habitual event was captured"), artifact line about a "captured seizure" that does not exist, impression identical to M02 and RM01, a per-finding `clinical_correlation` that interprets. | FIXED: limitations "Sleep-deprived recording of about 60 minutes with drowsiness and NREM stages N1-N2; no habitual event captured."; artifact impact without the seizure; F8/T4 localization and frequency; own numbered impression; `clinical_correlation` empty. |
| E | minor | `initial_tool_outputs.eeg.impression` | Impression without the ABNORMAL opening and without a final period. | FIXED: report-style numbered impression, same content (right temporal slowing, equivocal F8/T4 sharp transients, no seizures). |
| C | major | `initial_tool_outputs.labs` (plan M) | Prolactin row reported with no timing relative to an event of the previous evening. | FIXED: prolactin row deleted (no other mention in the case). |
| B | minor | `initial_tool_outputs.labs.panels.CBC` | Hb 14.4 with Hct 38.9 gives MCHC 37 g/dL (impossible). | FIXED: Hct 42.6 (MCHC 33.8). |
| D | major | `followup_outputs[*]` literature (plans A, O) | Required literature criterion; output cites fabricated or misattributed sources (Vazquez 2003 title and pages, Benbadis 2004, Knake 2005) and makes case-shaped claims (3T detects HS in 15-20%). | FIXED: criterion `optional`, last; output rewritten with Fisher 2017, Peltola 2023 and Bernasconi 2019 (plan 1.1), general content only; follow-up last. Leak guard passes. |
| C | major | `followup_outputs[*]` drug check, `action-5-check-drug-interactions` (plan B) | Required by template with the CYP-induction evidence; output missed the SSRI-NSAID bleeding interaction with her ibuprofen and listed oxcarbazepine without the SSRI hyponatremia overlap. | FIXED: criterion `optional` with canonical evidence; output covers levetiracetam with sertraline (no PK interaction, mood effects), sertraline with ibuprofen (GI bleeding), carbamazepine lowering sertraline and oxcarbazepine hyponatremia; no em dashes. |
| A | major | `ground_truth.action_criteria` (plans E, H, T, 3.2) | MRI required `contrast: true`; ECG required with template evidence; doubled citations; rationale equal to label; template expected evidence. | FIXED: MRI `{protocol: epilepsy}`; ECG `optional`; one key per criterion (`[ILAE_MRI_2019]`, `[IFCN_ILAE_EEG_2023]`, `[NICE_NG217_2025]`, `[ILAE_2017]`); short labels, case-specific rationales and evidence naming the stored results; order MRI, routine EEG, sleep-deprived EEG, labs, ECG, drug check, literature. |
| A | major | `ground_truth.sequence_constraints`, `stop_rule` (plans C, D) | MRI -> drug check soft constraint with the "low-grade tumor CYP-neutral" reason; stop rule with literature, drug check, ECG and `max_additional_actions: 0`. | FIXED: constraint deleted (drug check optional); stop rule MRI + routine EEG, max 2. |
| C | major | `ground_truth.assessment` (plan L) | Process musts (video-EEG, 3T MRI), a diagnostic-insight must, an ASM list including oxcarbazepine and lacosamide as first line; bupropion prohibition unrelated to the case. | FIXED: musts first-line lamotrigine or levetiracetam (reason: anxiety disorder, childbearing potential), contraception and folic acid, reassess the anxiety diagnosis and the sertraline increase, driving (canonical), safety and sleep, SUDEP; bupropion prohibition deleted, valproate prohibition (canonical) added, LP prohibition reworded without em dash. |
| C | major | `ground_truth.differential` (plan P) | PNES and panic `moderate` after an abnormal sleep-deprived EEG and right HS. | FIXED: both `low`, key features naming the excluding findings; frontal lobe epilepsy and syncope entries cite the EEG, MRI and ECG. |
| D | major | `ground_truth.key_clinical_evidence` (plans G, S) | Two engineering lines ("Tier per the July 2026 clinical review", "July 2026 review applied end to end"); claims about 3T, FDG-PET and a visuospatial memory deficit that the case does not serve. | FIXED: six case-specific items (semiology, two-seizure definition met by the auras, sleep-deprived EEG, standard MRI insensitive, febrile seizure, EEG and MRI concordance). |
| B | major | `ground_truth.red_herrings` | [0] pointed at `mri.additional_observations[3]` of the replaced 1.5T study; [2] recommended video-EEG. | FIXED: [0] now the outside 1.5T MRI in `patient.history_present_illness` (path and data point checked); [2] data point matches the routine impression and points to the sleep-deprived EEG; [1] unchanged apart from wording. |
| C | minor | `ground_truth.avoided_actions` (plan I) | Shared template rationales, one citation for all. | FIXED: case-specific rationales; CT waste kept (no head injury, deficit or anticoagulation, back to baseline, MRI available) with `[ILAE_MRI_2019]`; TTE and Holter `[NICE_NG217_2025]`. |
| A | minor | `fallback_tool_outputs.echo` (plan Q) | Echo fallback without `echo_type`. | FIXED: `echo_type: TTE`; discriminator guard passes. |
| C | minor | `patient.history_present_illness` | Left-hand manual automatisms with a right temporal focus (unilateral manual automatisms are usually ipsilateral). | FLAGGED, not changed: unilateral automatisms without contralateral dystonia lateralize weakly and discordant hand use occurs; no field uses the hand for localization (KCE states that localization rests on EEG and MRI concordance). |
| E | minor | `metadata.difficulty_rationale`, `estimated_complexity`, `revision_reason`, `last_revised` | Template text promising escalation to 3T MRI and video-EEG. | FIXED: case-specific text, last revised 2026-10-24. |

## Changes, in one paragraph a physician can read before re-reviewing

The scored MRI is now the dedicated 3T epilepsy-protocol study and shows definite right hippocampal sclerosis (2.5 vs 3.5 cm3, T2/FLAIR hyperintensity, lost internal architecture, mild temporal horn enlargement) without contrast; the earlier equivocal standard 1.5T MRI moved into the history as an outside study read as two nonspecific frontal white matter foci, which is now the imaging red herring. The routine EEG (right temporal slowing and equivocal F8/T4 sharp transients) stays required, and the recommended sleep-deprived EEG shows right anterior temporal sharp waves; its limitations no longer describe a captured event. FDG-PET left the pathway (ordering it is waste; the report is served as a fallback). Prolactin was removed, the hematocrit corrected. Labs, ECG, drug check and literature are optional; the drug check now reports the sertraline-ibuprofen bleeding risk and the effect of inducers on sertraline, and the literature cites only real ILAE and IFCN sources. Musts: lamotrigine or levetiracetam first line (anxiety, childbearing potential), contraception and folic acid, reassess the anxiety diagnosis, driving, safety, SUDEP; prohibitions add valproate and drop bupropion. PNES and panic are `low`.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys outside the pack allow-list used per plan 1.1: `[ILAE_MRI_2019]`, `[IFCN_ILAE_EEG_2023]`, `[NICE_NG217_2025]` (plan 5.2).
- Synonyms and ICD list (plan 5.6): the inherited list contains `G40.219` (intractable) and idiopathic `G40.009`/`G40.019`, which do not fit this non-intractable structural epilepsy.
- MRIReport has no technique field; the technique is the first `additional_observations` line.

## Open questions for Andrea (judgment calls you could not settle)

None. Decisions taken: the outside standard MRI was placed three months before presentation (the plan suggests "two years ago"; the HPI timeline of 8-10 months of spells and a PCP visit four months ago makes a recent outside study more coherent). The valproate prohibition was added although the plan's M01 line does not list it, because she is a 41-year-old woman of childbearing potential.

## Verification

Adversarial check, 24 Oct 2026 (case committed in b8be2153; read in full against the pre-round version fa1d22e6 and plan section 4).
- Checked: every own-finding row against the file (MRI rewrite, volumetry 2.5/3.5 cm3 = 29% smaller and (L-R)/(L+R) = 0.17; Hct 42.6 with Hb 14.4 = MCHC 33.8; prolactin absent everywhere; PET only as `FDG_PET` fallback plus waste avoided action; literature sources and titles real (Fisher 2017, Peltola 2023, Bernasconi 2019); tiers, order and stop rule per plan; no constraints; red-herring paths hold their data points; canonical valproate, driving and SUDEP texts; echo `echo_type`). Volumetric numbers and the PET ratio are not shared with another FEPI case. Musts do not contradict prohibitions or avoided actions; the differential matches the final evidence.
- Found: the log's last C row is wrong in substance. Left-hand manual automatisms with a right temporal focus are ipsilateral, which is the usual pattern (plan fact 12), so the sign is concordant, not discordant; no case change was needed and none was made.
- Changed: nothing in the case. `perfect_agent.py -v` and `case_io.py check` clean for this case; case guards pass.

## Condition audit

Condition auditor, 24 Oct 2026. Checked uniformity of the plan's decisions across the 30 cases and the FND and MS-RR audit classes (engineering text, any-query outputs, second-tier labs, copied numbers, sharp-wave durations, differential codes). After the changes below, `perfect_agent.py` and `case_io.py check` are clean for all 30 cases and `test_case_guards.py -k FEPI-TEMP` passes.

- `initial_tool_outputs.literature_search.general`: neutral focal-epilepsy block added (definition, classification, MRI protocol, first-line ASM, drug resistance), so a literature query that names no case-specific topic no longer receives a stored follow-up.

## Close-out (24 Oct 2026)

Condition close-out (`plans/FEPI-TEMP-decisions.md`). What changed and why:

- Diagnosis synonyms (`diagnosis_synonyms.yaml` G40 entries, re-applied with `--prune --conditions focal_epilepsy_temporal`): labels now focal epilepsy, temporal lobe epilepsy, TLE, epilepsy temporal lobe, mesial temporal lobe epilepsy, MTLE (added), mesial temporal sclerosis epilepsy; removed focal seizures; focal onset seizures; focal impaired awareness seizures (seizure-type labels, retired: their tokens occur in an acute symptomatic or functional-seizure answer). Codes: G40.2, G40.1, G40.9 plus G40.209, G40.109, G40.909 (not intractable); the idiopathic G40.009 and G40.019 removed and the intractable codes removed.
- Checks: `perfect_agent.py -v` and `case_io.py check` clean; `test_case_guards.py -k FEPI-TEMP-` passes, now with the discriminator guard and the FEPI-TEMP banned strings.
