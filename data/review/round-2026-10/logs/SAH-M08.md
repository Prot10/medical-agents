# SAH-M08
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 5d5b5879-e5ba-44d0-96fc-79e098655dc3 | ALREADY-FIXED (nimodipine must present); timeline FIXED | The nimodipine must existed; replaced by the canonical MUST-NIMO wording (`required_recommendations[3]`). The "moderate vasospasm" the note relies on came from a TCD dated day 6 that cannot exist at this encounter: the TCD follow-up is now an admission baseline, post-ictus day 3 counted from the sentinel bleed, right MCA 112 cm/s with Lindegaard 2.6 (mildly elevated, below the vasospasm range), no vasospasm. |
| ee9a1623-1919-4650-a807-236ac826ff1d | FIXED | Migraine red herring (she has no migraine) replaced with the sentinel red herring: data_point "Sudden severe headache 3 days earlier attributed to stress", field path `patient.history_present_illness`, correct interpretation per plan. Pearl replaced: "A sudden, peak-in-seconds headache needs immediate non-contrast CT even when attributed to stress or migraine; a sentinel headache days before the major bleed is a missed opportunity." The note's "20 to 50% rebleed risk in the acute phase" was not written into the case: published early rebleeding rates for an unsecured ruptured aneurysm are lower (about 4 to 14% in the first 24 hours), and the literature output that stated "20-50% in first 24 hours" was deleted (plan C7). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.chief_complaint` | "Sentinel headache 3 days ago" gives the diagnostic interpretation in the chief complaint. | FIXED: "Sudden severe headache today; a similar sudden headache 3 days ago". |
| D | minor | `patient.history_present_illness` | "is concerned about SAH, specifically worried about whether her headache 3 days ago may have been a sentinel bleed" names the diagnosis. | FIXED: "is worried that the headache 3 days ago was a warning of something serious". |
| D | minor | `initial_tool_outputs.ct.additional_observations[2]` | "CT now consistent with second bleed 3 days after possible sentinel bleed - increased risk of rebleeding" (history and prognosis in a CT report). | FIXED: removed. |
| D | minor | CTA `angiography_findings` | "morphology consistent with recent rupture/rebleed" (clinical inference). | FIXED: "Irregular saccular aneurysm 4.2 x 3.8 mm with a daughter sac"; cervical arteries line added (no dissection) to support the differential. |
| D | major | `initial_tool_outputs.drug_interactions` | Template `general` block that repeats the drug criterion's expected evidence (leak guard failed). | FIXED: deleted; the check is answered by `request_nimodipine_escitalopram_interaction_check` (escitalopram QT effect and SSRI bleeding effect, lisinopril hypotension, levothyroxine none). The criterion accepts `drug: nimodipine` or `drug: escitalopram`; it stays `recommended` (C10). |
| D | minor | escitalopram check | "Current QTc 462 ms - borderline; escitalopram dose may need reduction" (patient-specific verdict in a drug check). | FIXED: generic QT and monitoring statements; sertraline as the lower-QT SSRI alternative. |
| B | major | TCD | Day 6 study with moderate vasospasm in a patient seen hours after the second bleed; protocol named MCA only. | FIXED: see note 5d5b5879; canonical protocol and recommendation. |
| C | major | telemetry | Template "rare malignant arrhythmias warrant intervention", 24 h. | FIXED: 3 h since arrival, sinus 78 to 104/min, 12 PACs, no sustained arrhythmia or pauses. |
| C | major | musts | EVD must although the CT reports no hydrocephalus (carry-over); two 24-72 h securing musts; no home-drug decision with lisinopril stopped and an SSRI. | FIXED: EVD must removed; MUST-SECURE (right MCA bifurcation), MUST-ICU, MUST-BP-A (172/100), home-drug must (do not restart lisinopril acutely, continue levothyroxine, continue escitalopram with daily QTc), MUST-DCI. |
| C | minor | `ground_truth.red_herrings[0]` | Correct interpretation says the echocardiogram shows apical ballooning, but this echo is normal (LVEF 60%). | FIXED: data point names troponin 0.08 and T-wave inversions V2 to V4; interpretation says the echo shows normal wall motion. |
| C | minor | `ground_truth.differential` | RCVS `moderate` after CTA shows the aneurysm; template key features. | FIXED: RCVS `low` (recurrent thunderclap headaches named as the overlap); primary thunderclap headache `very_low`; dissection, CVST and SIH key features cite the case's results. |
| B | minor | labs | TSH placed inside the BMP; no magnesium; abnormal summary interpretive ("stress leukocytosis") and missing BNP; template type-and-screen text. | FIXED: TSH moved to a `Thyroid` panel (value unchanged, relevant to her hypothyroidism); magnesium 2.1 mg/dL added; factual abnormal list; `clinical_significance` null. |
| A | minor | criteria | No DSA; template rationales and evidence; free-text citations; literature recommended. | FIXED: `dsa-aneurysm-anatomy` (recommended) with a diagnostic DSA follow-up (4.3 x 3.8 mm, 1.4 mm daughter sac, neck 2.5 mm, M2 trunks at the neck base, single aneurysm, no vasospasm); plan 1.3 rationales and case-specific evidence; literature `optional` and last with the canonical output; sentinel literature deleted; echo `echo_type` TTE. |
| B | minor | `sequence_constraints`, `stop_rule` | None; stop rule allowed 0 extra actions. | FIXED: NCCT before CTA, CTA before DSA (soft); stop rule = the four required criteria, `max_additional_actions` 1. |
| E | minor | `metadata` | Stale CSF concern; template difficulty rationale. | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

The chief complaint and HPI no longer call the first headache a sentinel bleed; the agent must make that inference. The pathway is NCCT, labs (magnesium added, TSH in its own panel), ECG, CTA (cervical arteries reported clear), a new diagnostic DSA, the nimodipine and escitalopram interaction check, echo, telemetry (3 h of sinus rhythm), then optional TCD (admission baseline on day 3 from the sentinel, no vasospasm) and optional literature. The EVD must is gone (no hydrocephalus). The musts are: securing the right MCA bifurcation aneurysm as early as feasible, preferably within 24 hours; enteral nimodipine; neuro-ICU; IV short-acting agents for BP 172/100; not restarting lisinopril acutely, while continuing levothyroxine and escitalopram with daily QTc; sodium; and DCI surveillance. The troponin red herring now matches the normal echo, and a second red herring scores the stress attribution of the first headache. RCVS is now `low`.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `[Molyneux_2002]` in the canonical literature output needs the criteria-pack allow-list (plan 5.1).

## Open questions for Andrea (judgment calls you could not settle)

- The label keeps "Fisher 2-3" (plan section 6 question 5). The CT describes thin-to-moderate Sylvian and moderate suprasellar blood without a thickness, so I left the range rather than guess a value.

## Verification

Adversarial verifier, 24 Oct 2026. Read the log, plan C1 to C14 and section 4 M08, and the whole final case.

Checked: both note ids present. 5d5b5879: nimodipine must present (canonical wording); TCD is an admission baseline (day 3 from the sentinel, right MCA 112 cm/s, Lindegaard 2.6, "No sonographic evidence of vasospasm"). ee9a1623: sentinel red herring and pearl present with the plan wording; the declined "20 to 50%" figure is not in the case and the reason given (lower early rebleeding rates) is sound. The EVD must is gone and the CT reports no hydrocephalus or IVH; LP avoided action `harm` (CT-positive without IVH or hydrocephalus, per C6). No initial drug or literature block; escitalopram check has real content, its alternative argument matches the trigger; CTA (4.2 x 3.8 mm) and DSA (4.3 x 3.8 mm) agree; labs, abnormal summary and flags consistent; red herring now matches the normal echo; RCVS `low`; aspirin intolerance does not conflict with any must. Leak guards pass.

Found: nothing requiring a change. The label's "Fisher 2-3" range stays (plan section 6 question 5).

Re-ran `perfect_agent.py SAH-M08 -v` (pass) and `case_io.py check` (no failure names the case).

## Close-out (24 Oct 2026)

Condition close-out after Andrea's ruling of 24 Oct 2026 (open questions decided for dataset quality); decisions and sources in `plans/SAH-decisions.md`.

- `patient.neurological_exam.additional (Hunt-Hess grade removed)`: the Hunt-Hess grade is a SAH grading scale, so stating it in the patient block presupposes the diagnosis and does the agent's grading (decision Q8).
- `ground_truth.diagnosis.accepted[0] (Fisher 3)`: moderate suprasellar blood is a layer of 1 mm or more, Fisher 3; the CT now states the thickness and the label, CT and criterion evidence name one grade (Q5).
- `initial_tool_outputs.ct.additional_observations[0]`: moderate suprasellar blood is a layer of 1 mm or more, Fisher 3; the CT now states the thickness and the label, CT and criterion evidence name one grade (Q5).
- `initial_tool_outputs.ct.impression`: moderate suprasellar blood is a layer of 1 mm or more, Fisher 3; the CT now states the thickness and the label, CT and criterion evidence name one grade (Q5).
- `initial_tool_outputs.ct.findings[0].description`: moderate suprasellar blood is a layer of 1 mm or more, Fisher 3; the CT now states the thickness and the label, CT and criterion evidence name one grade (Q5).
- `action_criteria[NCCT].expected_evidence`: moderate suprasellar blood is a layer of 1 mm or more, Fisher 3; the CT now states the thickness and the label, CT and criterion evidence name one grade (Q5).
- fallback_tool_outputs.mri: SAH-consistent brain MRI instead of the library normal report: an off-pathway brain MRI was answered by the library normal report (no blood on SWI), contradicting the CT; the case fallback now reports the CT's blood on FLAIR and SWI (CENTRAL 10).
- `ground_truth.key_clinical_evidence` (late-presentation pearl removed): the 'Late presentation (>24 h) ... xanthochromia persists for weeks' pearl misstated the 6-hour threshold and the two-week persistence and duplicated the canonical CT and LP pearls (Q11).
- fallback_tool_outputs.cardiac_monitoring: 24 h Holter replaced by the case's own telemetry report: a 24-hour Holter cannot exist at assessment time; an off-pathway monitoring order now returns the case's own telemetry (CENTRAL 9).
- followup_outputs: MR angiography report added before the literature output (aneurysm site and size from the DSA, 0.2 mm smaller as TOF reads it; P02 negative): an MRA order was answered by a fallback reporting no abnormality, contradicting the CTA and DSA (CENTRAL 10). MRA stays a waste action after the CTA.
- `ground_truth.diagnosis` (synonyms re-expanded with `--prune`): diagnosis_synonyms.yaml: the I60 category no longer grants I60.8 (non-aneurysmal SAH), so the code was pruned from this aneurysmal case.
- Checks after the close-out: `perfect_agent.py` pass, `case_io.py check` schema and synonym guard OK with no failure naming the case, `test_case_guards -k SAH-` pass.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.specialized_test` set to null: a generic report (test_type '', impression 'No diagnostic abnormality identified on this study.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality '', impression 'No abnormality identified.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.
