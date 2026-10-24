# PD-RS02
Reviewer status: R1 none, R2 none (PD has no notes file; only the July 2026 tool review, `condition_tool_guidance.yaml` key `parkinsons`) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No physician note exists for PD. The case was corrected against plans/PD.md (classes C1 to C23, per-case entry PD-RS02) and the July 2026 tool review (MRI required; ECG, EEG, autonomic and tilt testing removed; labs, neuropsychology and genetics optional and targeted). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | major | `action-3-search-medical-literature`, `followup_outputs[0]`, `followup_outputs[2]` | Required literature criterion with an exact `query`; outputs with an invented author ("Defined et al."), Curran and Lang given as Arch Neurol 1994, a misattributed Bugalho paper (C1, ruling 5). | FIXED: criterion and both follow-ups deleted, removed from the stop rule; initial and fallback literature null. |
| A | major | `action-2-check-drug-interactions`, drug follow-up | Required drug check with an exact `drug` string; output advised separating iron (not taken) and listed agonist doses as "alternatives" (C2). | FIXED: `check_drug_interactions {}`, `optional`; one stored output `initial_tool_outputs.drug_interactions.general` (sertraline C2 sentence for a later MAO-B inhibitor; amlodipine orthostatic sentence; metformin and aspirin no relevant interaction); follow-up deleted, fallback null. |
| A | major | `action-1-analyze-brain-mri` | Required `{"contrast": false, "protocol": "standard"}` (C5); generic evidence "No vascular, structural, or NPH features"; bare key. | FIXED: `analyze_brain_mri {}`; canonical label and rationale plus the shunt question; `[Postuma_2015]`; evidence restates the report (catheter in place, Evans 0.27, Fazekas 1). |
| D | minor | `initial_tool_outputs.mri` | "No surrounding edema or enhancement" on a non-contrast study (C12); "functioning right VP shunt" (a functional inference); "appropriate for age and vascular risk factors" (clinical reference in a report); finding typed "Normal brain parenchyma" while describing white matter foci. | FIXED: enhancement removed; "right VP shunt catheter in situ"; Fazekas 1 foci without the clinical clause; finding retyped; numbered impression. |
| D | minor | `patient.history_present_illness` | "His most recent surveillance imaging was unremarkable with stable ventricular size" gives the result of the MRI question the case scores, with no date. | FIXED: the last surveillance scan is dated 3 years ago, before the current symptoms; no result given. |
| B | minor | `patient.neurological_exam.mental_status` | MoCA 27/30 with only two lost points listed (Trail B, delayed recall). | FIXED: one point each on Trail B, phonemic fluency and delayed recall. |
| B | major | `followup_outputs` (missing) | Exam MoCA 27/30, library battery returns MoCA 28 "average" (C9). | FIXED: stored battery (`request_neuropsych_testing`): MoCA 27, low-average Trail B and phonemic fluency, other domains preserved, GDS 4/15 (on sertraline); no criterion. |
| C | major | `ground_truth.avoided_actions`, `followup_outputs` (missing) | No stored DaTscan: the library would return "normal", an MDS absolute exclusion (C8). | FIXED: DaTscan `waste` (`avoid-waste-datscan`, NICE NG71 rationale) with a stored C8 report (left putamen 1.10, right 1.41; left deficit opposite the worse right side). |
| E | minor | every criterion `rationale`, `citations` | Rationale a copy of the label; bare duplicate keys (C3). | FIXED. |
| C | major | `ground_truth.assessment.required_recommendations` | Template musts; "Confirm clinically established PD" on one supportive criterion (rest tremor) before any levodopa (C6, C16); no shunt-specific point. | FIXED: five musts: C6 probable PD; check a programmable valve setting after MRI; canonical levodopa start; canonical agonist caution (62 years); physiotherapy for turning near-falls and speech therapy for hypophonia. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Overlapping D2 prohibitions with an em dash; a generic anticholinergic prohibition for "older adults or cognitive impairment" that does not describe this 62-year-old with MoCA 27. | FIXED: canonical D2 prohibition; new case-specific prohibition against attributing the parkinsonism to shunt failure or arranging revision with normal ventricles; generic anticholinergic line removed. |
| C | minor | `ground_truth.differential` | Shunt entry coded G91.2 (NPH) for obstructive hydrocephalus; five entries without ICD codes; likelihoods not updated to the normal MRI. | FIXED: "Parkinsonism from shunt failure with recurrent obstructive hydrocephalus" G91.1 `very_low` with the MRI data; ICD codes added; all alternatives `very_low` with excluding data (DLB: sleep talking only, no dream enactment). |
| D | major | `ground_truth.key_clinical_evidence` | Two "July 2026" engineering sentences (C4); "clinically established PD"; em dash. | FIXED: five case-specific lines. |
| B | minor | `ground_truth.red_herrings` | Path pointed at the whole PMH list. | FIXED: `past_medical_history[0]`, interpretation rewritten. |
| B | minor | `ground_truth.avoided_actions` | One-phrase rationales; no autonomic or tilt guard. | FIXED: case-specific rationales; DaTscan, autonomic and tilt `waste` added. |
| B | minor | `ground_truth.stop_rule` | Literature and drug ids listed; `max_additional_actions` 0 (C20). | FIXED: MRI only; 2. No sequence constraint (DaTscan is waste). |
| A | minor | `fallback_tool_outputs.echo`, `.ecg` | Echo without `echo_type` and "benign incidental finding"; ECG rate 79 against a resting HR of 68 (C17). | FIXED: `echo_type` TTE, concrete text, `fallback_tool_kinds.echo` "normal"; ECG "Sinus rhythm 68/min, normal axis and intervals, no ST change." |
| E | minor | `metadata.difficulty_description`, `.difficulty_rationale`, `.revision_reason`, `.last_revised` | "Straightforward case" in the description while `difficulty` is `moderate`; shared engineering text (C19). | FIXED: description no longer states a difficulty level (`difficulty` stays `moderate`: the shunt confounder justifies it, and other RS cases in the dataset are also moderate); case-specific rationale; revision reason; 2026-10-24. |
| - | check | plan 3.6 | perfect_agent ok (MRI from the initial output); case_io check: no failure names PD-RS02; test_case_guards 2 passed. Routing: DaTscan and battery return the case reports; `drug: levodopa` and `drug: rasagiline` return the case output; library PSG (normal) fits sleep talking without dream enactment; MIBG, amyloid, FDG, genetics, labs and orthostatic BP return library normals. | - |

## Changes, in one paragraph a physician can read before re-reviewing

This 62-year-old man with a VP shunt placed 10 years ago for aqueductal stenosis has an 18-month right-predominant parkinsonism with a re-emergent pill-rolling rest tremor, decrement, rigidity, micrographia, hypophonia and near-falls on turning; his father had PD. The policy is MRI only (required, any protocol), which shows the shunt catheter in place with normal ventricles; the literature step is gone, the medication review is optional (sertraline for a later MAO-B inhibitor, amlodipine), and a DaTscan is now waste because the clinical diagnosis is clear (a stored abnormal report keeps the data consistent). The HPI no longer reports the result of the prior surveillance scan; it dates it before the symptoms. The MRI no longer mentions enhancement on a non-contrast study. A battery matching MoCA 27 (point count corrected) is stored. The diagnosis is clinically probable PD, not "established". The musts are: probable PD; check a programmable valve after MRI; levodopa start; agonist warning; physiotherapy and speech therapy. A new prohibition forbids blaming the shunt with normal ventricles.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan R1: `[NICE_NG71]` (levodopa and agonist musts, DaTscan waste) is not yet in the PD criteria pack.
- Plan R5: the library MIBG default is normal; MIBG is not on this pathway, but a condition-aware default (reduced in PD) would be more coherent.

## Open questions for Andrea (judgment calls you could not settle)

- None specific to this case (plan Q1 to Q6 apply). Genetics was not added although his father had PD at 68: onset after 60 with one late-onset affected parent is not the young-onset or strong family history that Reviewer 1's tool review asks for; the library panel answer (negative) would not contradict the case if an agent ordered it.

## Verification (adversarial verifier, 24 Oct 2026)
- Read the log, the diff and the whole final case. No PD notes file exists.
- Checked: HPI no longer gives the result of the prior surveillance scan; MRI has no enhancement wording and states catheter position and Evans 0.27, matching the criterion, differential, red herring and the new prohibition; MoCA 27 point count (three single points) consistent with the stored battery; DaTscan waste with a stored left-putamen report opposite the right-sided signs; drug output names only his medicines (sertraline, amlodipine, metformin, aspirin); sleep talking only, so the library normal PSG fits; programmable-valve must present; probable PD; no sequence constraint (DaTscan waste); ECG fallback rate 68 equals the vital signs.
- No error found that needs a change. Nothing edited.
- Checks re-run after verification: `perfect_agent.py -v` pass; `case_io.py check` schema OK, no failure names the case; `test_case_guards -k` pass; MockServer routing: DaTscan, MIBG and amyloid return their own modality (case or library), PSG and battery return the case report where stored, `check_drug_interactions` with `drug: levodopa` and `drug: rasagiline` return the case output, labs route to the stored panel where one exists; grep for established / gadolinium / "Abnormal values:" / Lewy / serotonin syndrome / Tier per / July 2026 / dashes: only allowed hits.

## Close-out (24 Oct 2026)

Decisions in `plans/PD-decisions.md`.

- Accepted codes are now G20.A1 (PD without dyskinesia, without mention of fluctuations; also PD NOS) and G20; G20.A2, G20.B1, G20.B2 (motor complications the case does not have) and G20.C ("Parkinsonism, unspecified", not PD) are no longer accepted. Labels unchanged.
