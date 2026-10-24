# NPH-P07
Reviewer status: R1 none, R2 none (NPH was never annotated; no notes file; the only physician input is the July 2026 tool review, `condition_tool_guidance.yaml` key `nph`) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer note exists for this case. The July 2026 tool-review rulings (MRI with NPH markers required; tap test with opening pressure and pre/post gait required; generic CSF assays, advanced imaging and neuropsychology removed; labs optional) are applied through the plan classes below. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `ground_truth.red_herrings[1]`, `ground_truth.differential[leptomeningeal carcinomatosis]`, `ground_truth.assessment.prohibited_recommendations[4]`, `metadata.case_body_concerns` | Breast-cancer carry-over from P06 in a man with Gleason 6 prostate cancer on surveillance: "Past breast cancer" red herring, leptomeningeal carcinomatosis at moderate, a cytology prohibition, and the audit note about it (C15). | FIXED: all deleted; `case_body_concerns` cleared; no "breast", "tamoxifen" or "cytology" remains in the case content. |
| D | major | `patient.chief_complaint`, `patient.history_present_illness` | "tap trial was not offered" in the chief complaint; son "who has done research on PSP and NPH ... requesting LP and possibly tap trial"; "re-review ... shows Evans index 0.36" (the index MRI result) (C3). | FIXED: chief complaint without tap or NPH; "His son brought printed notes on balance disorders to the visit" (plan); prior MRI "reported as showing 'possible midbrain atrophy'; the images are not available". The wife's sentence no longer carries the reasoning "not the classic backward falls of PSP"; falls stated as three forward, one sideways. |
| D | major | `patient.neurological_exam.gait`, `.mental_status` | TUG and MoCA in the exam; falls reasoning in capitals inside the gait line (C4). | FIXED: qualitative gait and mental status, "reported separately". |
| B | minor | `patient.neurological_exam.cranial_nerves` | Content kept (mild slowing of upward saccades, normal downward saccades, no palsy); wording tidied (capitals, dash) and "full range" stated, which the old "NO complete vertical gaze palsy" implied but did not say. | FIXED: wording only. See Open questions on the saccade finding. |
| D | major | `initial_tool_outputs.clinical_assessment` | Baseline report held the post-tap results and "positive tap test" (C6). | FIXED: baseline only (TUG 34 s, 10-m 26 s, MoCA 22/30, freezing, en-bloc turn, retropulsion with recovery, falls, urgency). |
| A | major | `followup_outputs`, `ground_truth.action_criteria` | No post-tap reassessment and no case cognitive screen (C6). | FIXED: `request_post_reassessment` (recommended) and `request_moca_cognitive_screen` (optional, subscores sum to 22). |
| C | major | `initial_tool_outputs.mri` | "Evans index 0.36, missed on prior community read" (cross-study commentary); "MPAR 0.55" labelled as a midbrain-pons area ratio (an area ratio is about 0.12-0.24; 0.55 is a diameter ratio); no technique, temporal horns, Fazekas or MTA (C7, C8). | FIXED: technique; Evans 0.36; temporal horns; both DESH components; callosal angle 80; Fazekas 1; prominent aqueductal flow void; midbrain AP 10.4 mm, pons 18.9 mm, midsagittal midbrain-to-pons diameter ratio 0.55, no hummingbird or morning glory sign; MTA 1; canonical impression. |
| C | major | `followup_outputs[search_medical_literature]`, `[check_drug_interactions]` | Literature step with a numbered PSP-versus-NPH essay and "tap trial is diagnostic"; finasteride perioperative drug check (C1, C2). | FIXED: deleted. |
| B | minor | `initial_tool_outputs.csf` | RBC without unit; recital interpretation calling the tap "positive" (C5). | FIXED: "RBC 0/mcL"; canonical interpretation with the case figures. |
| B | minor | `initial_tool_outputs.labs` | PSA summary interpretive ("known Gleason 6 ... stable") and filed under "Metabolic"; HIV engineering row (C9). | FIXED: PSA value and reference only, in "Tumour markers"; "Serology"; `clinical_significance` null; factual interpretation. |
| B | minor | `fallback_tool_outputs.ct` | CT fallback normal against ventriculomegaly (C18). | FIXED: enlarged ventricles, Evans about 0.36. |
| C | major | `ground_truth.assessment` | Four process musts; wrong DESH/triad prohibition; AD, normal-ageing and cytology prohibitions (C11, C12). | FIXED: musts are referral with the figures and falls prevention (four falls); prohibitions canonical ventriculomegaly, the PSP-label prohibition with the Massey threshold, and do not withhold tap or referral because of the PSP label. |
| C | major | `ground_truth.differential` | VCI and PSP high; PD, AD, atrophy moderate after DESH, normal midbrain measures and a 32% tap response (C13). | FIXED: all low, with case-data reasons (PSP: mild isolated upward slowing, forward falls, ratio 0.55, tap response). |
| B | minor | `ground_truth.red_herrings` | PSP red herring data point not the visible PMH text. | FIXED: quotes the PMH; second red herring added for the eye-movement finding in the exam, which is what anchored the label. |
| A | minor | `ground_truth.action_criteria`, `avoided_actions`, `sequence_constraints`, `stop_rule`, `key_clinical_evidence` | Literature criterion; four-panel labs; label = rationale; bare citations; missing avoided entries; max 0; tier sentence and "sensitivity 50-80%" (C1, C9, C10, C19). | FIXED: plan 3.1-3.5 structure; key evidence includes F10 [Massey_2013]. |
| E | minor | `metadata.difficulty_variant_description`, `.difficulty_rationale` | "diagnosis reversed by formal neuro-ophthalmology" (no such step); "misdiagnosed for 2.5 years" (the label is 18 months old); counts out of date. | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

A 74-year-old man labelled PSP 18 months ago on mild upward-saccade slowing, falls and a "possible midbrain atrophy" report. The patient block no longer gives the index MRI's Evans index, the son's NPH research or any tap wording; the exam keeps the eye findings (full range, mild slowing of upward saccades only, normal downward saccades, no palsy) and the qualitative magnetic gait. The breast-cancer carry-over from P06 is gone. The work-up reads brain MRI, optional labs, baseline timed gait, optional MoCA, tap test and post-tap reassessment. MRI: Evans 0.36, DESH, callosal angle 80 degrees, temporal horns enlarged, prominent aqueductal flow void, midbrain 10.4 mm with a midbrain-to-pons diameter ratio of 0.55 and no hummingbird sign, Fazekas 1, MTA 1. Tap: opening pressure 16 cmH2O, normal CSF, 40 mL removed, TUG 34 to 23 s (32%), 10-m walk 26 to 17 s, MoCA 22 to 25. Musts: shunt referral on these data and falls prevention. Prohibitions: no iNPH from ventriculomegaly alone; do not keep the PSP label without a supranuclear gaze palsy or a ratio below 0.52; do not withhold the tap or the referral because of the label. The differential (PSP, PD, VCI, AD, atrophy) is all low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys `[Nakajima_2021]` and `[Massey_2013]` used per plan 1.1 (CENTRAL R2).
- `accepted[0]` "... prior PSP label not supported" left unchanged (plan R6).
- Post-tap criterion pattern equals the baseline criterion (plan R4).

## Open questions for Andrea (judgment calls you could not settle)

Plan question 5 answered: the exam shows no vertical supranuclear gaze palsy, so the label "PSP not supported" stands and the exam was not edited in substance. Recorded caveat: MDS-PSP 2017 counts slow vertical saccades (O2) as an ocular core feature, and with repeated falls within 3 years (P1) that would read as probable PSP-RS. I kept PSP low because the slowing here is mild, upward only, with normal downward saccades and full range (isolated upgaze impairment is common with ageing, while O2 asks for vertical slowing clearly beyond horizontal and beyond age), and because the MRI measures, the forward falls and the 32% tap response all point away from PSP. If a physician reviewer reads mild upward slowing as O2, the case would need to become iNPH with possible PSP copathology (a label change) rather than "PSP not supported".

## Verification
Adversarial verifier, 24 Oct 2026. No reviewer notes exist for NPH. Read the log, the diff against the pre-round version and every clinical field of the final case. Checked: breast-cancer carry-over fully gone (no breast, tamoxifen or cytology anywhere); midbrain 10.4 mm / pons 18.9 mm = 0.55 as stated, no hummingbird sign, and the Massey_2013 threshold used correctly in the prohibition, differential and key evidence; tap figures (TUG 34/26/23 s = 24%/32%, 10-m 26/17 s = 35%, MoCA 22/25) identical across reports, criteria and musts; exam (full vertical range, mild upward slowing only, normal downward saccades, no palsy) matches plan F10/question 5, and the worker's MDS-PSP caveat is recorded in the log.
Found and fixed:
- `patient.history_present_illness`: "mildly slow vertical saccades" contradicted the exam and the red herring, where only upward saccades are slow and downward saccades are normal (the distinction the "PSP not supported" label rests on). Now "mildly slow upward saccades".
- `followup_outputs[request_moca_cognitive_screen].findings[Attention]`: "5/6: serial 7s with one error" scores 6/6; now "5/6: two errors on letter tapping; serial 7s with one error". Total 22 unchanged.
- `fallback_tool_outputs.echo`: no `echo_type` (PATTERNS 5). Set to "TTE".
No other defect found. Checks run after the edits: `perfect_agent.py -v` passes (every required and recommended criterion served by a case output, no fallback or library answer); `case_io.py check` clean for the case; `test_case_guards -k` passes (leak, follow-up and banned-string guards); MockServer hijack sequence (cognitive screen, then baseline gait "before tap test", MRI, CSF "large-volume lumbar puncture", post-tap reassessment, second CSF call) returns the baseline, the tap report and the post-tap follow-up in the right places; patient-block grep for Evans, callosal, DESH, NPH, hydroceph, tap, shunt, TUG, MoCA finds only hits allowed by C3/C4.

## Condition audit (NPH auditor, 24 Oct 2026)
- `action-post-tap-gait-reassessment.rationale` was the template sentence shared verbatim by P03 to P07; now case-specific (tap volume and what the reassessment separates).
- Checks after the edits: `perfect_agent.py` passes for all 30 NPH cases, `case_io.py check` clean.

## Close-out (24 Oct 2026)

Condition close-out (`plans/NPH-decisions.md`); no clinical data the agent receives changed.
- Synonyms (`diagnosis_synonyms.yaml`, applied with `--prune --conditions nph`): code G91.0 removed (ICD-10-CM communicating hydrocephalus, which covers secondary NPH, a different entity from iNPH); labels unchanged, G91.2 and G91.9 accepted.
- Label (ruling 3, plan R6): `accepted[0]` "Idiopathic normal pressure hydrocephalus (iNPH), dash, prior PSP label not supported" -> "Idiopathic normal pressure hydrocephalus (iNPH)". The reasoning stays where it belongs (differential, prohibitions, key evidence); ICD code G91.2 unchanged; scoring unchanged (the synonyms already carried it).
- `key_clinical_evidence`: the 10% TUG threshold is no longer attributed to `[Nakajima_2021]`, which sets no numeric tap-test cut-off; it is stated as a commonly used threshold that no guideline fixes (the tap protocol keeps its Nakajima citation where the sentence states it).
- Checks: `perfect_agent.py -v` pass, `case_io.py check` clean, `test_case_guards -k NPH-` pass. Not yet in `DISCRIMINATOR_CONDITIONS`: the post-tap follow-up's prose `assessment_type` is deliberate until the timing discriminator lands (CENTRAL C2 in the decisions file).
