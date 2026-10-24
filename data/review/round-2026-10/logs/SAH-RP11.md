# SAH-RP11
Reviewer status: R1 none, R2 approved | Approved before this round: yes

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 9b8af8ad-26de-47af-8c4a-f75fa4f755a8 | FIXED | Securing: the 24-72 h must is replaced by MUST-SECURE for the right posterior communicating artery aneurysm (`required_recommendations[3]`), pearl `key_clinical_evidence[8]` replaced. DSA: new recommended criterion `dsa-aneurysm-anatomy` with a diagnostic DSA follow-up (`followup_outputs[1]`, 4.9 x 4.2 mm, neck 2.8 mm, dome-to-neck 1.8, no vasospasm). Timeline: the day-5 TCD with mild vasospasm (MFV 128) is now a post-ictus day 0 normal baseline with the canonical protocol and recommendation. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | minor | `patient.history_present_illness` | Reasoning in the HPI: "headaches are not typical of an MS relapse" and "The thunderclap onset is atypical for an MS relapse or PML." | FIXED: both removed; the HPI keeps the neurologist's PML concern and the JCV index as history. |
| D | minor | `initial_tool_outputs.ct` | "MS white matter lesions visible but not relevant" and "Known MS white matter lesions" interpret for the agent (C14); no statement on intraventricular blood. | FIXED: neutral "bilateral periventricular white matter hypodensities, nonspecific"; "No intraventricular hemorrhage" added to observations and impression. |
| C | major | `initial_tool_outputs.labs` | Lymphocytes as a string "0.8 x10^9/L (low-normal due to natalizumab)" flagged abnormal inside a 1.0-4.0 range; natalizumab raises circulating lymphocytes rather than lowering them; interpretive "Lymphopenia from natalizumab (expected)" in the summary. | FIXED: numeric 4.4 x10^9/L, flagged high, no interpretive text; summary and interpretation list the same three abnormal values. |
| B | minor | `initial_tool_outputs.labs` | No potassium, magnesium or PTT (C9); "Exclusion studies" panel; type-and-screen engineering sentence (C14). | FIXED: potassium 4.0, magnesium 2.0, PTT 31 s; panel deleted, numeric BNP 42 in Cardiac; type-and-screen significance null. |
| C | major | `followup_outputs[drug check]` | Claimed "JC virus PCR in CSF was negative - PML excluded" though no LP was done; no home-drug guidance on baclofen or lisinopril. | FIXED: report lists lisinopril additive hypotension, no abrupt baclofen withdrawal, natalizumab timing with the MS neurologist, no parenteral nimodipine. Criterion stays recommended with a case-specific label, rationale and evidence. |
| C | major | `required_recommendations` | No home-medication must; BP must carried a target (C4). | FIXED: MUST-BP-B (146/86); must to withhold lisinopril, continue baclofen and plan natalizumab with the MS neurologist. |
| B | minor | `followup_outputs[MRI]`, `action_criteria` | MRI follow-up existed without a criterion; plan 3.1 keeps RP11's MRI recommended. | FIXED: recommended criterion `mri-brain-ms-natalizumab` (no arguments, matches the follow-up); MRI report rewritten without interpretation: FLAIR SAH, non-enhancing MS lesions without restricted diffusion, no asymmetric subcortical lesion. |
| B | minor | `followup_outputs[CTA]` | Neck CTA silent on the cervical arteries although dissection is in the differential. | FIXED: "No dissection" in findings and impression; DSA recommended in place of treatment content. |
| B | minor | `followup_outputs[telemetry]` | Template telemetry (C12). | FIXED: 3-hour report, sinus 78-104 bpm, 4 isolated PVCs, no sustained arrhythmia, no pauses (QTc 458 below the 480 threshold). |
| D | major | `followup_outputs[literature]` | MS-specific literature follow-up with unverifiable content; criterion recommended (C7). | FIXED: deleted; canonical literature last; criterion `optional`, last. |
| C | major | musts, prohibitions, pearls | Daily TCD must, nimodipine and BP prohibitions in old wording, CT and LP pearls (C4, C5). | FIXED: MUST-NIMO, MUST-ICU, MUST-DCI, sodium must kept; canonical nimodipine and BP prohibitions (MS prohibition kept); CT, LP, securing and DCI pearls replaced. |
| C | minor | `ground_truth.differential` | "MS-related Lhermitte / headache flare" (not a recognized entity); pituitary entry cited a pituitary MRI; PML absent. | FIXED: MS relapse and PML (very low) with this case's MRI findings; pituitary canonical wording; RCVS and dissection entries cite this case's CT and CTA. |
| B | minor | `ground_truth.red_herrings` | Template troponin red herring; no red herring for the MS/PML anchoring the HPI invites. | FIXED: troponin 0.10 with T inversions V1-V4 and normal echo; new MS/PML red herring pointing to the HPI. |
| A | minor | `ground_truth.action_criteria[*]`, `sequence_constraints`, `stop_rule` | Label-copied rationales, unbracketed citations, plan order not followed. | FIXED: canonical rationales and citations; order per plan 3.1; NCCT before CTA and CTA before DSA (soft); stop rule = four required criteria, `max_additional_actions` 1. |

## Changes, in one paragraph a physician can read before re-reviewing

A 40-year-old woman with relapsing MS on natalizumab (JCV index 3.2), on lisinopril and baclofen, seen 2 hours after a thunderclap headache; Fisher 3 SAH and a 4.8 x 4.2 mm right PComA aneurysm with a bleb. The HPI no longer argues against MS relapse or PML; the CT describes the white matter lesions neutrally and states no IVH; lymphocytes are 4.4 (high, as natalizumab causes), with potassium, magnesium, PTT and BNP added. The CTA states no dissection; a recommended DSA confirms the anatomy without treatment content; a recommended MRI shows FLAIR SAH and non-enhancing MS lesions with nothing suggesting PML. The drug check no longer claims a CSF JCV PCR that was never done and covers lisinopril, baclofen and natalizumab timing, which a new must repeats. The TCD is a normal admission baseline instead of a day-5 vasospasm study. Musts: nimodipine, securing as early as feasible preferably within 24 hours, ICU, BP monitoring (146/86), home drugs, sodium, DCI surveillance. Telemetry is a real report; the literature step is optional and canonical; the differential now lists PML.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `[Molyneux_2002]` used in the canonical literature output (plan section 5.1b allow-list request).
- Review UI: initial outputs and follow-ups in criterion order (plan section 5.5).

## Open questions for Andrea (judgment calls you could not settle)

- Lymphocytes changed from 0.8 to 4.4 x10^9/L because natalizumab raises circulating lymphocytes; confirm the value, or keep a normal count if you prefer no abnormal lymphocyte value.
- Natalizumab: the must defers the next infusion timing to the MS neurologist rather than fixing a hold; confirm this is the wording you want.

## Verification

Adversarial check (24 Oct 2026). Read the log, the diff and the whole final case. Note 9b8af8ad present and verified FIXED (MUST-SECURE, DSA 4.9 x 4.2 mm vs CTA 4.8 x 4.2 mm, diagnostic only; TCD day 0). Also verified: the "JC virus PCR in CSF was negative" claim is gone (no LP in the case); lymphocytes 4.4 flagged high against 1.0-4.0, in step with summary and interpretation (natalizumab-induced lymphocytosis is correct physiology); baclofen continued, lisinopril withheld, natalizumab timing deferred to the MS neurologist in both the must and the check; MS relapse and PML in the differential, very low, with the MRI findings that exclude them; CT white matter lesions described neutrally; MUST-BP-B for 146/86; stop rule equals the four required criteria; guards pass.
Found and fixed: the `mri-brain-ms-natalizumab` rationale stated a rule that does not exist ("A high JC virus antibody index on natalizumab calls for MRI before the next infusion is given"). Rewritten as "On natalizumab with a high JC virus antibody index, MRI is the surveillance test for PML; an MRI during the admission documents the MS lesion burden and screens for a new lesion before the next infusion is planned."
perfect_agent.py SAH-RP11 -v: pass; case_io.py check: clean for SAH-RP11.

## Close-out (24 Oct 2026)

Condition close-out after Andrea's ruling of 24 Oct 2026 (open questions decided for dataset quality); decisions and sources in `plans/SAH-decisions.md`.

- `patient.neurological_exam.additional (Hunt-Hess grade removed)`: the Hunt-Hess grade is a SAH grading scale, so stating it in the patient block presupposes the diagnosis and does the agent's grading (decision Q8).
- fallback_tool_outputs.cardiac_monitoring: 24 h Holter replaced by the case's own telemetry report: a 24-hour Holter cannot exist at assessment time; an off-pathway monitoring order now returns the case's own telemetry (CENTRAL 9).
- followup_outputs: MR angiography report added before the literature output (aneurysm site and size from the DSA, 0.2 mm smaller as TOF reads it; P02 negative): an MRA order was answered by a fallback reporting no abnormality, contradicting the CTA and DSA (CENTRAL 10). MRA stays a waste action after the CTA.
- `ground_truth.diagnosis` (synonyms re-expanded with `--prune`): diagnosis_synonyms.yaml: the I60 category no longer grants I60.8 (non-aneurysmal SAH), so the code was pruned from this aneurysmal case.
- Checks after the close-out: `perfect_agent.py` pass, `case_io.py check` schema and synonym guard OK with no failure naming the case, `test_case_guards -k SAH-` pass.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- follow-up `request_echocardiogram`: `echo_type` set to `TTE` (was missing); the bedside study is transthoracic, and untyped it also answered a TEE or bubble-study order.
- `fallback_tool_outputs.specialized_test` set to null: a generic report (test_type '', impression 'No diagnostic abnormality identified on this study.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality '', impression 'No abnormality identified.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.
